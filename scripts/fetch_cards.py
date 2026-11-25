"""Fetch syllabus cards listed in one public study plan on krk.prz.edu.pl.

krk.prz.edu.pl/robots.txt has `Disallow: /`. The team agreed (docs/tasks.md, ADR-001 risk 6)
to fetch only the cards linked from one public plan, once, with a delay between requests.
Already downloaded files are skipped, so re-runs do not hit the server for the same cards.

Usage:
    python scripts/fetch_cards.py            # whole plan (block AI, 51 cards)
    python scripts/fetch_cards.py --limit 3  # trial run
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PLAN_URL = (
    "https://krk.prz.edu.pl/plany.pl?lng=PL&W=E&K=F&KW=&TK=html&S=2424&P=&C=&erasmus=&O=T"
)
USER_AGENT = "prompt-engineering-rag/0.1 (student course project, syllabus RAG)"
MANIFEST_FIELDS = ["file", "mk", "course_name", "semester", "ects", "source_url", "retrieved_at", "sha256"]

ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
CARD_LINK_RE = re.compile(r'href="(https?://krk\.prz\.edu\.pl/karta\.pl\?mk=(\d+)[^"]*)"[^>]*>([^<]+)</a>')
TAG_RE = re.compile(r"<[^>]+>")


def fetch(url: str) -> tuple[int, str, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.geturl(), response.read()


def slugify(text: str) -> str:
    text = text.replace("ł", "l").replace("Ł", "L")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_plan(page: str) -> list[dict]:
    """Return one entry per card (mk), merging semesters when a card repeats."""
    cards: dict[str, dict] = {}
    for row in ROW_RE.findall(page):
        cells = CELL_RE.findall(row)
        link = CARD_LINK_RE.search(row)
        if not link or len(cells) < 9:
            continue
        url, mk, name = html.unescape(link.group(1)), link.group(2), html.unescape(link.group(3)).strip()
        semester = TAG_RE.sub("", cells[0]).strip()
        ects = TAG_RE.sub("", cells[8]).strip()
        card = cards.setdefault(mk, {"mk": mk, "course_name": name, "source_url": url, "semesters": [], "ects": []})
        card["semesters"].append(semester)
        card["ects"].append(ects)
    return list(cards.values())


def is_card(final_url: str, body: str) -> bool:
    return "cas.prz.edu.pl" not in final_url and "Karta zajęć" in body and "<h3" in body


def load_manifest(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        return {row["mk"]: row for row in csv.DictReader(f)}


def save_manifest(path: Path, rows: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for mk in sorted(rows, key=int):
            writer.writerow(rows[mk])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan-url", default=DEFAULT_PLAN_URL)
    parser.add_argument("--prefix", default="inf1-ai")
    parser.add_argument("--out", type=Path, default=Path("data/raw"))
    parser.add_argument("--manifest", type=Path, default=Path("data/manifest.csv"))
    parser.add_argument("--delay", type=float, default=2.5)
    parser.add_argument("--limit", type=int, default=None, help="download at most N new cards")
    args = parser.parse_args()

    status, _, body = fetch(args.plan_url)
    cards = parse_plan(body.decode("utf-8", errors="replace"))
    print(f"Plan: HTTP {status}, {len(cards)} kart z linkiem")

    args.out.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(args.manifest)
    downloaded = skipped = failed = 0

    for card in cards:
        if args.limit is not None and downloaded >= args.limit:
            break
        name = f"{args.prefix}_{card['mk']}_{slugify(card['course_name'])}.html"
        target = args.out / name
        if target.exists():
            skipped += 1
            continue
        time.sleep(args.delay)
        try:
            status, final_url, data = fetch(card["source_url"])
        except OSError as exc:
            print(f"  BLAD {card['mk']}: {exc}", file=sys.stderr)
            failed += 1
            continue
        text = data.decode("utf-8", errors="replace")
        if status != 200 or not is_card(final_url, text):
            print(f"  BLAD {card['mk']}: HTTP {status}, {final_url} nie wyglada na karte", file=sys.stderr)
            failed += 1
            continue
        target.write_bytes(data)
        manifest[card["mk"]] = {
            "file": name,
            "mk": card["mk"],
            "course_name": card["course_name"],
            "semester": ";".join(card["semesters"]),
            "ects": ";".join(card["ects"]),
            "source_url": card["source_url"],
            "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        downloaded += 1
        print(f"  OK {name} ({len(data)} B)")

    save_manifest(args.manifest, manifest)
    print(f"Pobrane: {downloaded}, pominięte (już są): {skipped}, błędy: {failed}, manifest: {args.manifest}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
