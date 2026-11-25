"""Runtime settings read from environment variables (.env in the repo root)."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# Library telemetry off before gradio / huggingface_hub are imported.
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


def _path(name: str, default: str) -> Path:
    path = Path(os.getenv(name, default))
    return path if path.is_absolute() else ROOT / path


RAW_DIR = ROOT / "data" / "raw"
SAMPLE_DIR = ROOT / "data" / "sample"
PROMPTS_DIR = ROOT / "prompts"
CHROMA_DIR = _path("CHROMA_DIR", "data/chroma")
RUN_LOG_PATH = _path("RUN_LOG_PATH", "experiments/results/runs.jsonl")

COLLECTION = "syllabi"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sdadas/mmlw-retrieval-roberta-large")
EMBEDDING_QUERY_PREFIX = os.getenv("EMBEDDING_QUERY_PREFIX", "zapytanie: ")
CHUNK_MAX_CHARS = int(os.getenv("CHUNK_MAX_CHARS", "1200"))
TOP_K = int(os.getenv("TOP_K", "5"))

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
LLM_SEED = int(os.getenv("LLM_SEED", "42"))
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1")
