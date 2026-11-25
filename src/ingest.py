"""Convert syllabus files to Markdown, remove personal data, chunk by section, index in Chroma.

Usage: .venv/bin/python src/ingest.py   (reads data/raw/, falls back to data/sample/)
"""

import re
from pathlib import Path

from docling.document_converter import DocumentConverter

import config
import index

SUPPORTED_SUFFIXES = {".html", ".htm", ".pdf", ".docx"}
REDACTED = "[usunięto]"

# Coordinator and per-semester lecturers: from the label up to the next Markdown heading.
_STAFF_BLOCK = re.compile(r"Imię i nazwisko koordynatora.*?(?=^#|\Z)", re.S | re.M)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PHONE = re.compile(r"\b(?:tel\.?|telefon)[:\s]*\+?[\d()][\d\s()-]{6,}\d", re.I)
_HEADING = re.compile(r"^#{1,6}\s+(.+)$")


def redact(markdown: str) -> str:
    """Remove lecturer names, e-mail addresses and phone numbers."""
    text = _STAFF_BLOCK.sub(f"Koordynator i prowadzący: {REDACTED}\n\n", markdown)
    text = _EMAIL.sub(REDACTED, text)
    return _PHONE.sub(REDACTED, text)


def _pack(blocks: list[str], max_chars: int) -> list[str]:
    """Join paragraphs into chunks of at most max_chars; split oversized blocks by line."""
    pieces: list[str] = []
    for block in blocks:
        if len(block) <= max_chars:
            pieces.append(block)
        else:
            pieces.extend(line for line in block.splitlines() if line.strip())
    chunks, current = [], ""
    for piece in pieces:
        if current and len(current) + len(piece) + 2 > max_chars:
            chunks.append(current)
            current = ""
        current = f"{current}\n\n{piece}" if current else piece
    if current:
        chunks.append(current)
    return chunks


def chunk_markdown(markdown: str, section: str, max_chars: int) -> tuple[list[tuple[str, str]], str]:
    """Split Markdown into (section, text) chunks. Returns chunks and the last section title."""
    chunks: list[tuple[str, str]] = []
    blocks: list[str] = []

    def flush() -> None:
        chunks.extend((section, text) for text in _pack(blocks, max_chars))
        blocks.clear()

    for block in re.split(r"\n\s*\n", markdown):
        block = block.strip()
        heading = _HEADING.match(block)
        if heading:
            flush()
            section = heading.group(1).strip()
        elif block and block != "<!-- image -->":
            blocks.append(block)
    flush()
    return chunks, section


def convert(path: Path, converter: DocumentConverter) -> tuple[str, list[tuple[int | None, str]]]:
    """Return the document title and Markdown per page (page None for HTML/DOCX)."""
    doc = converter.convert(path).document
    if doc.pages:
        parts = [(page, doc.export_to_markdown(page_no=page)) for page in sorted(doc.pages)]
    else:
        parts = [(None, doc.export_to_markdown())]
    first_heading = next(
        (m.group(1) for _, md in parts for line in md.splitlines() if (m := _HEADING.match(line))),
        path.stem,
    )
    return first_heading.strip(), parts


def source_files() -> list[Path]:
    for directory in (config.RAW_DIR, config.SAMPLE_DIR):
        files = sorted(p for p in directory.iterdir() if p.suffix.lower() in SUPPORTED_SUFFIXES)
        if files:
            return files
    return []


def main() -> None:
    files = source_files()
    if not files:
        raise SystemExit("Brak plików w data/raw/ i data/sample/.")
    print(f"Źródło: {files[0].parent.relative_to(config.ROOT)} ({len(files)} plików)")

    converter = DocumentConverter()
    ids, texts, metadatas = [], [], []
    for path in files:
        title, parts = convert(path, converter)
        section, n = "(początek)", 0
        for page, markdown in parts:
            page_chunks, section = chunk_markdown(redact(markdown), section, config.CHUNK_MAX_CHARS)
            for chunk_section, text in page_chunks:
                meta = {"source_file": path.name, "title": title, "section": chunk_section, "chunk": n}
                if page is not None:
                    meta["page"] = page
                ids.append(f"{path.name}::{n}")
                texts.append(f"Przedmiot: {title}\nSekcja: {chunk_section}\n\n{text}")
                metadatas.append(meta)
                n += 1
        print(f"  {path.name}: {n} chunków")

    stored = index.rebuild(ids, texts, metadatas)
    print(f"Zaindeksowano {stored} chunków w {config.CHROMA_DIR}")


if __name__ == "__main__":
    main()
