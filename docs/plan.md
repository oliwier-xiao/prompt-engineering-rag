# Plan pracy

Etapy zgodne z przebiegiem zajęć. Statusy aktualizujemy na bieżąco.

| Etap | Zadania | Status |
|---|---|---|
| Start | Temat wybrany (temat 12, wariant: sylabusy), repo, README, szkielet raportu | gotowe |
| Planowanie | Wybór UI (Gradio/Streamlit/Chainlit), modelu, embeddingów, wektorówki. Kryteria sukcesu. Zbiór sylabusów | gotowe (`docs/adr-001-stack.md`, `docs/tasks.md`) |
| Prototypowanie | Ingest + chunking, retrieval, prompt v1, UI z podglądem źródeł, tryb bez RAG | w toku (v0 w `src/`) |
| Iteracja | Zestaw `eval/`, porównanie bez RAG/z RAG, prompt v2 i v3, analiza porażek, ewentualnie zmiana chunkingu | |
| Finalizacja | Raport PDF, uporządkowanie repo, README | |
| Zaliczenie | Demo i odpowiedzi na pytania | |

## Kryteria sukcesu (robocze)

- Odmowa przy braku danych w testach poza bazą: wszystkie przypadki z `eval/` kategorii „odmowa”.
- Poprawna wartość i cytat dokumentu w pytaniach kategorii „odpowiedź w bazie”.
- Min. 3 wersje promptu z tabelą porównawczą wyników.
- Każda halucynacja z RAG opisana w raporcie z przyczyną.

## Otwarte decyzje

- [x] UI: Gradio vs Streamlit vs Chainlit -> Gradio 6.x (ADR-001)
- [x] LLM (darmowy z OpenRoutera czy inny) i polityka danych -> OpenRouter `:free` na start, tylko
  publiczne karty po usunięciu danych osobowych; docelowo Ollama (Bielik), zadanie T-06
- [x] Model embeddingów (obsługa polskiego) -> `sdadas/mmlw-retrieval-roberta-large`, baza ChromaDB, parser Docling
- [x] Zakres sylabusów (który kierunek, ile dokumentów) -> Informatyka, I stopień, stacjonarne, blok AI,
  cykl 2026/2027, 51 kart z `krk.prz.edu.pl` (kontrakt w `docs/tasks.md`); pobrane 2026-11-25
  skryptem `scripts/fetch_cards.py`, opis w `data/manifest.csv`
- [x] Metryka wierności (ręczna ocena vs LLM-as-judge) -> ręczna ocena obu osób; lokalny LLM-as-judge
  po przejściu na Ollama (T-10)
- [x] Skład zespołu i podział pracy -> Oliwier (rdzeń RAG, UI, prompty), Ignacy (dane, ewaluacja); `docs/tasks.md`
