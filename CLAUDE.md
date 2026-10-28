# Projekt: Uczelniany Asystent Sylabusów (RAG)

Laboratorium Prompt Engineering, temat 12 (RAG, poziom zaawansowany, ocena bazowa 5,0).
Pełny kontekst: `README.md`, `docs/projekt.md`, `docs/wymagania.md`, `docs/plan.md`.

## Dziennik promptów (OBOWIĄZKOWE)

Przedmiot wymaga dokumentowania promptów, iteracji, modeli i ustawień. Dziennik prowadzimy w
LaTeX-u od razu, nie na koniec: **`raport/sections/prompty.tex`**.

Po każdym prompcie użytkownika, który zmienia coś w projekcie (kod, dokumenty, dane, raport,
decyzje), dopisz wpis na końcu tego pliku, w tej samej turze, przed zakończeniem odpowiedzi.
Pomijaj tylko czyste pytania bez skutku w repo (np. „co robi ta funkcja?”).

Format wpisu (makra z `raport/preamble.tex`):

```latex
\promptentry{N}{RRRR-MM-DD}{Nazwa modelu (id modelu), narzędzie}{effort}{Krótki cel}
\begin{lstlisting}
Treść promptu (dosłownie albo z oznaczonym skrótem [...]).
\end{lstlisting}
\promptresult{Krótki opis rezultatu: co powstało, co zawiodło, co poprawiono.}
```

Zasady:

- `N` rośnie o 1; sprawdź ostatni numer w pliku.
- **Model i effort** bierz z bieżącej sesji (`/model`, `/effort`; nagłówek środowiska podaje
  nazwę i id modelu). Nie zgaduj: jeśli nie znasz wartości, wpisz `nieustalone`.
- Prompt wklejaj w `lstlisting` (bezpieczny dla znaków specjalnych LaTeX-a). Zrzuty ekranu i
  załączniki opisz słowami w nawiasie kwadratowym.
- Nie wpisuj sekretów, kluczy API ani danych osobowych. Zamiast nich `[usunięto]`.
- Wynik pisz konkretnie i uczciwie, także porażki (to materiał do sekcji analizy błędów).
- To jest log promptów używanych **do pracy nad projektem**. Prompty systemowe samego
  asystenta RAG (v1, v2, v3 ...) trzymamy w `prompts/` i opisujemy w sekcji o strategii promptowania.
- Po wpisie sprawdź kompilację: `cd raport && latexmk -pdf -outdir=build main.tex`.

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
- Stack (UI, LLM, embeddingi, wektorówka) **nie jest jeszcze zatwierdzony**: wybór po porównaniu
  Gradio / Streamlit / Chainlit. Do tego czasu nie dodawać zależności ani kodu aplikacji.

## Język

Dokumentacja i raport po polsku. Kod i identyfikatory po angielsku.
