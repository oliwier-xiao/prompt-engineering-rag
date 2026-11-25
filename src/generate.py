"""Answer a question in "Bez RAG" or "Z RAG" mode and log the run settings.

Usage: .venv/bin/python src/generate.py "Ile punktów ECTS ma ...?" [--no-rag]
"""

import argparse
import json
import subprocess
from datetime import datetime, timezone

from openai import OpenAI

import config
import index

PROMPT_MARKER = "\n## Prompt\n"


def load_system_prompt(version: str) -> str:
    text = (config.PROMPTS_DIR / f"{version}.md").read_text(encoding="utf-8")
    if PROMPT_MARKER not in text:
        raise ValueError(f"prompts/{version}.md: brak nagłówka '## Prompt'")
    return text.split(PROMPT_MARKER, 1)[1].strip()


def build_user_message(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return question
    fragments = "\n\n".join(
        f"[{i}] ({c['source_file']}, sekcja: {c['section']})\n{c['text']}"
        for i, c in enumerate(chunks, start=1)
    )
    return f"Fragmenty sylabusów:\n\n{fragments}\n\nPytanie: {question}"


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(config.ROOT), "describe", "--always", "--dirty"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _log(record: dict) -> None:
    config.RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with config.RUN_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def answer(question: str, use_rag: bool, prompt_version: str | None = None, log: bool = True) -> dict:
    """Return the answer, retrieved chunks and the settings used; append the run to the log."""
    prompt_version = prompt_version or config.PROMPT_VERSION
    if not config.LLM_MODEL or not config.LLM_API_KEY:
        raise RuntimeError("Ustaw LLM_MODEL i LLM_API_KEY w pliku .env (szablon: .env.example).")

    chunks = index.search(question, config.TOP_K) if use_rag else []
    messages = [
        {"role": "system", "content": load_system_prompt(prompt_version)},
        {"role": "user", "content": build_user_message(question, chunks)},
    ]
    settings = {
        "mode": "rag" if use_rag else "no_rag",
        "prompt_version": prompt_version,
        "llm_base_url": config.LLM_BASE_URL,
        "llm_model": config.LLM_MODEL,
        "temperature": config.LLM_TEMPERATURE,
        "seed": config.LLM_SEED,
        "top_k": config.TOP_K if use_rag else 0,
        "embedding_model": config.EMBEDDING_MODEL,
        "chunk_max_chars": config.CHUNK_MAX_CHARS,
        "git_commit": _git_commit(),
    }

    client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=config.LLM_TEMPERATURE,
        seed=config.LLM_SEED,
    )
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "question": question,
        "answer": response.choices[0].message.content or "",
        "served_model": response.model,
        "settings": settings,
        "sources": [
            {k: c[k] for k in ("source_file", "section", "page", "chunk", "score") if k in c}
            for c in chunks
        ],
    }
    if log:
        _log(record)
    return record | {"chunks": chunks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("question")
    parser.add_argument("--no-rag", action="store_true", help="tryb Bez RAG")
    args = parser.parse_args()
    result = answer(args.question, use_rag=not args.no_rag)
    print(result["answer"])
    for i, source in enumerate(result["sources"], start=1):
        print(f"[{i}] {source['source_file']} | {source['section']} | {source['score']}")


if __name__ == "__main__":
    main()
