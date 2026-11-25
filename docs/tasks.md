# Tablica zadań

Przed pracą sprawdź ten plik i trzymaj się zakresu przypisanego właścicielowi. Zmiany w plikach
wspólnych tylko przez pull request do `main`.

## Zakresy i gałęzie

| Właściciel | Gałąź | Pliki (wyłączny zapis) |
|---|---|---|
| [Oliwier] | `Oliwier-UI` | `src/**`, `prompts/**`, `requirements.txt`, `.env.example`, `experiments/**` |
| [Ignacy] | `Ignacy-data` | `data/raw/**` (tylko lokalnie), `data/manifest.csv`, `eval/**` |
| wspólne (PR) | `main` | `docs/**`, `CLAUDE.md`, `README.md`, `raport/**` |

## Flow pracy

1. Praca na swojej gałęzi (`Oliwier-UI` / `Ignacy-data`), przed startem
   `git pull --rebase origin main`.
2. Dziennik promptów: każdy pisze tylko do swojego pliku, `raport/sections/prompty/oliwier.tex`
   (O1, O2, ...) albo `raport/sections/prompty/ignacy.tex` (I1, I2, ...).
3. Status zadania w tej tablicy zmienia właściciel w tym samym PR, który zamyka zadanie.
4. PR do `main` = mały zakres; przed scaleniem kompilacja raportu
   (`cd raport && latexmk -pdf -outdir=build main.tex`) i ingest na `data/sample/`.
5. Bezpośrednio na `main` tylko zmiany organizacyjne uzgodnione przez obie osoby.

## Zadania

Statusy: `todo`, `w toku`, `gotowe`, `zablokowane`.

| ID | Właściciel | Zadanie | Pliki | Status |
|---|---|---|---|---|
| T-01 | [Oliwier] | Prototyp v0: ingest, chunking, indeks Chroma, tryby bez RAG / z RAG, UI Gradio | `src/**`, `requirements.txt`, `.env.example` | gotowe; wywołanie LLM do sprawdzenia po dodaniu klucza do `.env` |
| T-02 | [Oliwier] | Prompt v1 (bazowy) | `prompts/v1.md` | gotowe |
| T-03 | [Ignacy] | Pobranie 51 kart zajęć bloku AI zgodnie z kontraktem niżej, `data/manifest.csv` | `data/raw/**`, `data/manifest.csv` | w toku |
| T-04 | [Ignacy] | Kontrola danych osobowych: ingest na pełnym zbiorze, ręczny przegląd 5 losowych kart w indeksie | raport w PR | todo |
| T-05 | [Ignacy] | Zestaw `eval/questions.csv`: min. po 5 pytań w każdej z 5 kategorii z `eval/README.md` | `eval/**` | todo |
| T-06 | [Oliwier] | Przejście na Ollama: Bielik 11B (zapas 4.5B), aktualizacja `.env.example` i ADR | `.env.example`, `docs/adr-001-stack.md` (PR) | todo |
| T-07 | [Oliwier] | Skrypt wsadowy: pytania z `eval/` w obu trybach, wyniki do `experiments/results/` | `src/**`, `experiments/**` | todo |
| T-08 | [Oliwier] | Prompty v2 i v3 z opisem zmian | `prompts/v2.md`, `prompts/v3.md` | todo |
| T-09 | [Ignacy] | Ręczna ocena wyników (skala: poprawna / halucynacja / niepotrzebna odmowa + zgodność cytatu) | `eval/**` | todo |
| T-10 | [Ignacy] | Lokalny LLM-as-judge po T-06, porównanie z oceną ręczną | `eval/**` | todo |
| T-11 | [Oliwier] | Raport: architektura, strategia promptowania, techniki | `raport/sections/**` (PR) | todo |
| T-12 | [Ignacy] | Raport: dane, ewaluacja, analiza porażek | `raport/sections/**` (PR) | todo |
| T-13 | wspólne | Raport: zagrożenia, wnioski, podział pracy; prezentacja z demo | `raport/sections/**` (PR) | todo |

## Kontrakt danych: `data/raw/`

**Zakres.** Kierunek Informatyka, I stopień, stacjonarne, blok tematyczny AI - Sztuczna
inteligencja, cykl 2026/2027. Lista kart: plan studiów
`https://krk.prz.edu.pl/plany.pl?lng=PL&W=E&K=F&KW=&TK=html&S=2424&P=&C=&erasmus=&O=T`
(51 kart, parametr `mk` = kod zajęć).

**Pobieranie.** `krk.prz.edu.pl/robots.txt` zawiera `Disallow: /`, więc bez crawlera
i bez skryptów masowo pobierających strony. Karty zapisujemy ręcznie z przeglądarki
(„Zapisz stronę jako”, tylko HTML) albo po pisemnej zgodzie wydziału.

**Format.** Jeden plik = jedna karta zajęć. Preferowany oryginalny HTML
(`format=v1_html`). Dopuszczalne PDF z warstwą tekstową i DOCX. Bez skanów.

**Nazwa pliku.** Małe litery ASCII, bez spacji:
`inf1-ai_<mk>_<slug-nazwy>.html`, np. `inf1-ai_354_analiza-matematyczna-i-algebra-liniowa.html`.

**Manifest `data/manifest.csv`** (w gicie, bez danych osobowych), kolumny:

```
file,mk,course_name,semester,ects,source_url,retrieved_at,sha256
```

**Dane osobowe.** Pliki w `data/raw/` zostają lokalnie (katalog w `.gitignore`), nie trafiają
do gita ani do zewnętrznych usług w postaci surowej. Ingest (`src/ingest.py`) przed
indeksowaniem usuwa: blok od „Imię i nazwisko koordynatora” do następnego nagłówka sekcji
(koordynator i prowadzący w semestrach), adresy e-mail, numery telefonów. Do LLM trafiają
tylko fragmenty z indeksu. Po każdej zmianie zbioru: T-04 (ręczny przegląd próbki).

**Dane testowe.** `data/sample/` zawiera wyłącznie syntetyczne karty (fikcyjne treści
i osoby) do testu dymnego; ingest używa ich, gdy `data/raw/` jest pusty.
