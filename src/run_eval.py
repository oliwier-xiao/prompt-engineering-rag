"""Batch run: every question from a CSV in "Bez RAG" and "Z RAG" mode, results for manual grading.

Usage:
  .venv/bin/python src/run_eval.py                                  # eval/questions.csv, prompt from .env
  .venv/bin/python src/run_eval.py --questions data/sample/questions.csv --prompt v2

Writes two files to experiments/results/:
  <date>_<prompt>_<model>.jsonl  full records (answer, sources, settings)
  <date>_<prompt>_<model>.csv    sheet for manual grading (columns ocena, cytat_ok, uwagi left empty)
Question CSV columns: id, kategoria, pytanie, oczekiwane_zachowanie, zrodlo_w_bazie (eval/README.md).
"""

import argparse
import csv
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

from openai import RateLimitError

import config
import generate

MODES = {"no_rag": False, "rag": True}
DAILY_FREE_LIMIT = 50  # OpenRouter :free without purchased credits (docs/adr-001-stack.md)


def _ask(question: str, use_rag: bool, prompt: str, retries: int, backoff: float) -> dict:
    for attempt in range(retries + 1):
        try:
            return generate.answer(question, use_rag=use_rag, prompt_version=prompt, log=False)
        except RateLimitError:
            if attempt == retries:
                raise
            time.sleep(backoff * (attempt + 1))
    raise AssertionError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--questions", default="eval/questions.csv")
    parser.add_argument("--prompt", default=config.PROMPT_VERSION, help="wersja z prompts/, np. v2")
    parser.add_argument("--modes", default="no_rag,rag", help="no_rag, rag lub oba")
    parser.add_argument("--limit", type=int, default=0, help="tylko N pierwszych pytań (0 = wszystkie)")
    parser.add_argument("--delay", type=float, default=3.5, help="sekundy między zapytaniami (limit 20/min)")
    parser.add_argument("--retries", type=int, default=2, help="ponowienia po 429")
    args = parser.parse_args()

    questions_path = Path(args.questions)
    if not questions_path.is_absolute():
        questions_path = config.ROOT / questions_path
    with questions_path.open(encoding="utf-8", newline="") as f:
        questions = list(csv.DictReader(f))
    if args.limit:
        questions = questions[: args.limit]
    if not questions:
        raise SystemExit(f"Brak pytań w {questions_path}")
    modes = [m.strip() for m in args.modes.split(",")]
    if unknown := set(modes) - MODES.keys():
        raise SystemExit(f"Nieznany tryb: {', '.join(sorted(unknown))}")

    calls = len(questions) * len(modes)
    print(f"{len(questions)} pytań x {len(modes)} tryby = {calls} zapytań, model {config.LLM_MODEL}, prompt {args.prompt}")
    if calls > DAILY_FREE_LIMIT:
        print(f"Uwaga: więcej niż {DAILY_FREE_LIMIT} zapytań (dzienny limit darmowego konta).", file=sys.stderr)

    model_slug = re.sub(r"[^a-z0-9-]+", "-", config.LLM_MODEL.lower()).strip("-")
    stem = config.ROOT / "experiments" / "results" / f"{date.today()}_{args.prompt}_{model_slug}"
    stem.parent.mkdir(parents=True, exist_ok=True)

    rows, errors = [], 0
    with stem.with_suffix(".jsonl").open("a", encoding="utf-8") as jsonl:
        for q in questions:
            for mode in modes:
                started = time.monotonic()
                meta = {key: q.get(key, "") for key in ("id", "kategoria", "pytanie", "oczekiwane_zachowanie", "zrodlo_w_bazie")}
                try:
                    result = _ask(q["pytanie"], MODES[mode], args.prompt, args.retries, backoff=20)
                    result.pop("chunks", None)
                    record = {**meta, **result, "latency_s": round(time.monotonic() - started, 1)}
                except Exception as exc:  # one failed question must not stop the batch
                    errors += 1
                    record = {**meta, "settings": {"mode": mode, "prompt_version": args.prompt}, "error": f"{type(exc).__name__}: {exc}"}
                jsonl.write(json.dumps(record, ensure_ascii=False) + "\n")
                jsonl.flush()
                rows.append({
                    "id": meta["id"],
                    "kategoria": meta["kategoria"],
                    "tryb": mode,
                    "pytanie": meta["pytanie"],
                    "oczekiwane_zachowanie": meta["oczekiwane_zachowanie"],
                    "odpowiedz": record.get("answer", record.get("error", "")),
                    "zrodla": "; ".join(f"{s['source_file']} | {s['section']}" for s in record.get("sources", [])),
                    "ocena": "",
                    "cytat_ok": "",
                    "uwagi": "",
                })
                print(f"  {meta['id']} {mode}: {'BŁĄD' if 'error' in record else 'ok'} ({time.monotonic() - started:.1f}s)")
                time.sleep(args.delay)

    with stem.with_suffix(".csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wyniki: {stem.with_suffix('.jsonl').relative_to(config.ROOT)}, {stem.with_suffix('.csv').relative_to(config.ROOT)} (błędy: {errors})")


if __name__ == "__main__":
    main()
