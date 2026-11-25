# ADR-001: Stack prototypu RAG

- **Status:** zaakceptowany
- **Data:** 2026-11-25
- **Decydenci:** Oliwier, Ignacy
- **Źródła:** research z 2026-11-25 (PyPI, GitHub, Hugging Face, dokumentacja dostawców), raport
  w `raport/sections/prompty/oliwier.tex`, wpis O5.

## Kontekst

Prototyp ma odpowiadać na pytania o sylabusy w dwóch trybach (bez RAG i z RAG), cytować
źródła, odmawiać przy braku danych i zapisywać ustawienia każdego uruchomienia
(`docs/wymagania.md`). Zakaz z wymagań: nie wysyłać do zewnętrznych usług danych osobowych,
poufnych ani objętych ograniczeniami licencyjnymi.

Korpus: karty zajęć kierunku Informatyka (I stopień, stacjonarne, blok tematyczny
AI - Sztuczna inteligencja) z `krk.prz.edu.pl`, cykl 2026/2027, 51 kart. Karty są publiczne,
dostępne tylko jako HTML (`karta.pl?mk=<id>&format=v1_html`). Każda karta zawiera imię
i nazwisko koordynatora oraz prowadzących.

## Decyzja

| Warstwa | Wybór | Wersja |
|---|---|---|
| UI | Gradio, `gr.ChatInterface`, źródła jako wiadomość z `metadata.title` (zwijany panel) | `>=6.32,<7` |
| LLM (start) | OpenRouter, `nvidia/nemotron-3.5-super-vl:free` (dostawca: Nvidia), model w `.env` (`LLM_MODEL`), klient zgodny z API OpenAI | `openai>=2,<3` |
| LLM (docelowo) | Ollama lokalnie, `SpeakLeash/bielik-11b-v3.1-instruct:Q4_K_M`, zapas `bielik-4.5b-v3.0-instruct:Q8_0` | zadanie T-06 w `docs/tasks.md` |
| Embeddingi | `sdadas/mmlw-retrieval-roberta-large` (1024 wym., 512 tokenów, Apache-2.0), prefiks zapytań `zapytanie: ` | `sentence-transformers>=5,<6` |
| Baza wektorowa | ChromaDB, `PersistentClient` w `data/chroma/`, odległość kosinusowa | `>=1.5.9,<2` |
| Parser | Docling (HTML, PDF, DOCX; tabele do Markdown) | `>=2.150,<3` |
| Środowisko | `uv`, Python 3.12, `requirements.txt` z przypiętymi wersjami | |
| Ewaluacja | ręczna ocena przez obie osoby: poprawna / halucynacja / niepotrzebna odmowa + zgodność cytatu; po przejściu na Ollama dodatkowo lokalny LLM-as-judge | |

Przejście OpenRouter -> Ollama nie wymaga zmian w kodzie: Ollama udostępnia API zgodne
z OpenAI (`http://localhost:11434/v1`), zmienia się tylko `LLM_BASE_URL`, `LLM_API_KEY`
i `LLM_MODEL` w `.env`.

## Uzasadnienie

- **Gradio:** natywny podgląd kroków pośrednich w czacie (wiadomość z `metadata`), aktywne
  wydania (6.32.0 z 2026-11-12), wskazany przez prowadzącego. Wersja 7 jest w fazie dev,
  dlatego górna granica `<7`.
- **OpenRouter na start:** decyzja zespołu (szybki start bez pobierania modeli 5-7 GB).
  Dopuszczalny, bo wysyłamy wyłącznie fragmenty publicznych kart zajęć po usunięciu danych
  osobowych (patrz Ryzyka).
- **mmlw-retrieval-roberta-large:** najlepszy wynik w polskim benchmarku wyszukiwania PIRB
  (NDCG@10 = 58,46) spośród sprawdzonych modeli, licencja Apache-2.0, 870 MB.
- **ChromaDB:** trwały zapis lokalny, filtry po metadanych, od 1.5.4 bez telemetrii.
- **Docling:** jedno API dla HTML, PDF i DOCX, tabele (efekty uczenia się, nakład pracy,
  sposób oceniania) zachowane jako tabele Markdown, licencja MIT. Dla HTML nie pobiera modeli.

## Odrzucone alternatywy

| Opcja | Powód odrzucenia |
|---|---|
| Chainlit | repozytorium zarchiwizowane 2026-10-15, projekt bez gwarancji utrzymania |
| Streamlit | równorzędny, ale historię czatu i panel źródeł trzeba składać ręcznie |
| Google AI Studio bezpośrednio | darmowy tier: trenowanie na danych i przegląd przez ludzi |
| PyMuPDF | licencja AGPL-3.0, DOCX tylko w płatnej wersji Pro |
| pdfplumber + python-docx | dwa narzędzia, tabele trzeba składać do tekstu ręcznie |
| pypdf | brak ekstrakcji tabel |
| FAISS, sqlite-vec, LanceDB, Qdrant local | więcej kodu (FAISS) lub brak przewagi przy korpusie ok. 50 dokumentów |
| `BAAI/bge-m3`, `multilingual-e5-base` | zapasowe; słabsze lub cięższe dla polskiego wyszukiwania |

## Ryzyka

1. **Prywatność (OpenRouter).** Darmowe modele obsługują zewnętrzni dostawcy, a ich polityki
   mogą dopuszczać trenowanie na danych. Przykład: darmowy `google/gemma-4-31b-it:free` idzie
   przez Google AI Studio, którego warunki dla usług bezpłatnych dopuszczają trenowanie
   i przegląd przez ludzi. Środki: (a) wysyłamy tylko fragmenty publicznych kart zajęć,
   (b) ingest usuwa imiona i nazwiska koordynatora i prowadzących oraz adresy e-mail
   i telefony przed indeksowaniem, (c) w ustawieniach prywatności OpenRouter wyłączamy
   logowanie promptów, (d) nie wysyłamy danych użytkowników ani innych plików,
   (e) przejście na Ollama (T-06) jako cel.
2. **Dostępność modeli `:free`.** 2026-11-25: `google/gemma-4-31b-it:free` i `gemma-4-26b-a4b-it:free`
   zwracały stale 429 (wspólna pula Google AI Studio), dlatego start na Nemotronie. Płatna
   `google/gemma-4-31b-it` (ok. 0,0005 USD za zapytanie z RAG) odłożona: konto bez kredytów.
   Lista zmienia się często, limit 20 zapytań/min i 50 dziennie
   (1000 po zakupie min. 10 kredytów). Model zawsze w `.env`, nigdy na sztywno w kodzie.
3. **Jakość polszczyzny modeli `:free`** nieznana [niezweryfikowane]; mierzymy na `eval/`.
4. **Odtwarzalność.** Modele `:free` nie gwarantują determinizmu. Każde zapytanie zapisuje
   w `experiments/results/runs.jsonl`: model, `base_url`, temperaturę, seed, `top_k`, model
   embeddingów, wersję promptu, commit git i źródła.
5. **Limit 512 tokenów embeddingów.** Chunki do ok. 1200 znaków.
6. **`robots.txt` serwisu `krk.prz.edu.pl` ma `Disallow: /`.** Automatyczne pobieranie jest
   wykluczone; karty pobieramy ręcznie (51 plików) albo po uzyskaniu zgody wydziału.
7. **Sprzęt.** RTX 4050 6 GB: Bielik 11B Q4_K_M (6,7 GB) nie zmieści się w całości w VRAM
   [niezweryfikowane: szybkość nie mierzona]. Sprzęt drugiej osoby nieznany.
