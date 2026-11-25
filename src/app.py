"""Gradio UI: chat with a "Z RAG" / "Bez RAG" switch and a collapsible source preview.

Usage: .venv/bin/python src/app.py
"""

import config  # noqa: F401  (loads .env and disables telemetry before gradio import)
import gradio as gr

from generate import answer

MODE_RAG = "Z RAG"
MODE_NO_RAG = "Bez RAG"


def _settings_line(settings: dict) -> str:
    return (
        f"Tryb: {settings['mode']} · model: `{settings['llm_model']}` · "
        f"temperatura: {settings['temperature']} · seed: {settings['seed']} · "
        f"prompt: {settings['prompt_version']} · top_k: {settings['top_k']}"
    )


def _sources_markdown(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        page = f", s. {c['page']}" if "page" in c else ""
        parts.append(
            f"**[{i}] {c['source_file']}** · {c['section']}{page} · podobieństwo {c['score']}\n\n"
            f"```text\n{c['text']}\n```"
        )
    return "\n\n".join(parts)


def respond(message: str, history: list, mode: str) -> list[gr.ChatMessage]:
    # Each question is answered independently; history is not sent to the model in v0.
    try:
        result = answer(message, use_rag=(mode == MODE_RAG))
    except Exception as exc:  # shown to the user instead of a silent UI error
        return [gr.ChatMessage(role="assistant", content=f"Błąd: {exc}")]

    reply = [gr.ChatMessage(role="assistant", content=result["answer"])]
    details = _settings_line(result["settings"])
    if result["chunks"]:
        details += "\n\n" + _sources_markdown(result["chunks"])
        title = f"Źródła ({len(result['chunks'])})"
    else:
        title = "Ustawienia (bez źródeł)"
    reply.append(gr.ChatMessage(role="assistant", content=details, metadata={"title": title}))
    return reply


demo = gr.ChatInterface(
    respond,
    title="Asystent sylabusów (prototyp v0)",
    description="Pytania o karty zajęć. Tryb „Z RAG” odpowiada na podstawie zaindeksowanych sylabusów i pokazuje źródła.",
    additional_inputs=[gr.Radio([MODE_RAG, MODE_NO_RAG], value=MODE_RAG, label="Tryb")],
    additional_inputs_accordion=gr.Accordion("Tryb odpowiedzi", open=True),
)

if __name__ == "__main__":
    demo.launch()
