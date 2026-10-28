# Plan pracy

Etapy zgodne z przebiegiem zajęć. Statusy aktualizujemy na bieżąco.

| Etap | Zadania | Status |
|---|---|---|
| Start | Temat wybrany (temat 12, wariant: sylabusy), repo, README, szkielet raportu | w toku |
| Planowanie | Wybór UI (Gradio/Streamlit/Chainlit), modelu, embeddingów, wektorówki. Kryteria sukcesu. Zbiór sylabusów | |
| Prototypowanie | Ingest + chunking, retrieval, prompt v1, UI z podglądem źródeł, tryb bez RAG | |
| Iteracja | Zestaw `eval/`, porównanie bez RAG/z RAG, prompt v2 i v3, analiza porażek, ewentualnie zmiana chunkingu | |
| Finalizacja | Raport PDF, uporządkowanie repo, README | |
| Zaliczenie | Demo i odpowiedzi na pytania | |

## Kryteria sukcesu (robocze)

- Odmowa przy braku danych w testach poza bazą: wszystkie przypadki z `eval/` kategorii „odmowa”.
- Poprawna wartość i cytat dokumentu w pytaniach kategorii „odpowiedź w bazie”.
- Min. 3 wersje promptu z tabelą porównawczą wyników.
- Każda halucynacja z RAG opisana w raporcie z przyczyną.

## Otwarte decyzje

- [ ] UI: Gradio vs Streamlit vs Chainlit
- [ ] LLM (darmowy z OpenRoutera czy inny) i polityka danych
- [ ] Model embeddingów (obsługa polskiego)
- [ ] Zakres sylabusów (który kierunek, ile dokumentów)
- [ ] Metryka wierności (ręczna ocena vs LLM-as-judge)
- [ ] Skład zespołu i podział pracy
