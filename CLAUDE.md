# Projekt: Uczelniany Asystent Sylabusów (RAG)

Laboratorium Prompt Engineering, temat 12 (RAG, poziom zaawansowany, ocena bazowa 5,0).
Pełny kontekst: `README.md`, `docs/projekt.md`, `docs/wymagania.md`, `docs/plan.md`.

## Dziennik promptów (OBOWIĄZKOWE)

Przedmiot wymaga dokumentowania promptów, iteracji, modeli i ustawień. Dziennik prowadzimy w
LaTeX-u od razu, nie na koniec. Każda osoba ma własny plik (brak konfliktów przy scalaniu):

| Osoba | Plik | Numeracja |
|---|---|---|
| Oliwier | `raport/sections/prompty/oliwier.tex` | O1, O2, ... |
| Ignacy | `raport/sections/prompty/ignacy.tex` | I1, I2, ... |

Kim jest użytkownik, ustal z `git config user.name`; gdy nie pasuje do żadnej osoby, zapytaj.
Pisz tylko do pliku tej osoby. `raport/sections/prompty.tex` jedynie dołącza oba pliki: nie
dopisuj tam wpisów.

Po każdym prompcie użytkownika, który zmienia coś w projekcie (kod, dokumenty, dane, raport,
decyzje), dopisz wpis na końcu swojego pliku, w tej samej turze, przed zakończeniem odpowiedzi.
Pomijaj tylko czyste pytania bez skutku w repo (np. „co robi ta funkcja?”).

Format wpisu (makra z `raport/preamble.tex`):

```latex
\promptentry{O1}{RRRR-MM-DD}{Nazwa modelu (id modelu), narzędzie}{effort}{Krótki cel}
\begin{lstlisting}
Treść promptu (dosłownie albo z oznaczonym skrótem [...]).
\end{lstlisting}
\promptresult{Krótki opis rezultatu: co powstało, co zawiodło, co poprawiono.}
```

Zasady:

- Numer: prefiks osoby (`O`/`I`) + kolejny numer; sprawdź ostatni wpis w swoim pliku.
- Nowy etap pracy: `\subsubsection*{Etap ...}` przed pierwszym wpisem etapu.
- **Model i effort** bierz z bieżącej sesji (`/model`, `/effort`; nagłówek środowiska podaje
  nazwę i id modelu). Nie zgaduj: jeśli nie znasz wartości, wpisz `nieustalone`.
- Prompt wklejaj w `lstlisting` (bezpieczny dla znaków specjalnych LaTeX-a). Zrzuty ekranu i
  załączniki opisz słowami w nawiasie kwadratowym.
- Nie wpisuj sekretów, kluczy API ani danych osobowych. Zamiast nich `[usunięto]`.
- Wynik pisz konkretnie i uczciwie, także porażki (to materiał do sekcji analizy błędów).
- To jest log promptów używanych **do pracy nad projektem**. Prompty systemowe samego
  asystenta RAG (v1, v2, v3 ...) trzymamy w `prompts/` i opisujemy w sekcji o strategii promptowania.
- Po wpisie sprawdź kompilację: `cd raport && latexmk -pdf -outdir=build main.tex`.

## LaTeX: skill `latex-engineer`

Skill jest w repo: `.claude/skills/latex-engineer/` (kopia autorskiego skilla, Claude Code ładuje go
automatycznie po sklonowaniu). Przy każdej pracy nad plikami `.tex` korzystaj z niego i trzymaj
format raportu:

- `raport/main.tex` zawiera tylko `\input{preamble}` i `\input{sections/...}`. Pakiety i makra są
  w `raport/preamble.tex`, pogrupowane funkcyjnie (język, typografia, grafika, kod, bibliografia).
- Jedna sekcja = jeden plik w `raport/sections/`, numerowany (`01-...`). Dziennik promptów w
  `sections/prompty.tex` (dodatek), wpisy w `sections/prompty/<osoba>.tex`.
- Tabele przez `booktabs` (bez pionowych linii). Polskie cudzysłowy `,,tekst''`, twarde spacje po
  jednoliterowych spójnikach (`a~to`). Kod i prompty w `lstlisting` (styl `prompt`).
- Styl inżynierski, bez „AI slopu”: konkret zamiast przymiotników, strona czynna, liczby zamiast
  „znacząco”.
- Bibliografia tylko ze zweryfikowanych źródeł (DOI lub strona źródła). Wymagania przedmiotu nie
  są pozycją bibliograficzną (są w `docs/wymagania.md`).
- Kompilacja: `cd raport && latexmk -pdf -outdir=build main.tex`.
- Nowy plik `.tex` zakładaj w tym samym układzie. Dla szablonów poza raportem patrz
  `.claude/skills/latex-engineer/templates/`.

## Oznaczanie treści AI

Treści w raporcie wygenerowane lub istotnie przekształcone przez AI oznaczamy makrem `\aigen{}`
albo opisem w sekcji o użyciu GenAI. Zespół weryfikuje każdy wynik. Kod wygenerowany przez model
uruchamiamy, testujemy i przeglądamy pod kątem bezpieczeństwa.

## Reguły danych

- Nie wysyłać do zewnętrznych usług danych osobowych, poufnych ani objętych ograniczeniami
  licencyjnymi. Surowe sylabusy w `data/raw/` są poza gitem.
- Cytowania w `raport/bib/zrodla.bib` wyłącznie zweryfikowane. Niepewne oznaczać
  `% TODO: verify`.

## Struktura

- `src/` kod RAG, `prompts/` wersje promptów systemowych, `eval/` pytania testowe,
  `experiments/` wyniki bez RAG / z RAG, `raport/` LaTeX, `docs/` wymagania, opis, plan.
- `data/sample/` syntetyczne karty do testu dymnego, `data/manifest.csv` opis zbioru (bez PII).

## Stack (zatwierdzony, `docs/adr-001-stack.md`)

- UI: Gradio 6.x (`<7`). LLM: OpenRouter `:free` przez klienta `openai` (model tylko w `.env`),
  docelowo Ollama (Bielik); zmiana przez `LLM_BASE_URL`/`LLM_MODEL`, bez zmian w kodzie.
- Embeddingi: `sdadas/mmlw-retrieval-roberta-large` (prefiks zapytań `zapytanie: `).
  Baza: ChromaDB w `data/chroma/`. Parser: Docling. Python 3.12 w `.venv` przez `uv`.
- Uruchomienie: `.venv/bin/python src/ingest.py`, potem `.venv/bin/python src/app.py`.
- Do LLM trafiają tylko fragmenty z indeksu po usunięciu danych osobowych (ingest). Nowe
  zależności: przypięta wersja w `requirements.txt`, wpis w ADR przy zmianie warstwy stacku.

## Podział pracy

Przed pracą sprawdź `docs/tasks.md` i trzymaj się zakresu przypisanego właścicielowi.

## Język

Dokumentacja i raport po polsku. Kod i identyfikatory po angielsku.
