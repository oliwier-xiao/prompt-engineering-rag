# Tablica zadań

Przed pracą sprawdź ten plik i trzymaj się zakresu przypisanego właścicielowi. Zmiany w plikach
wspólnych tylko przez pull request do `main`.

## Zakresy i gałęzie

| Właściciel | Gałąź | Pliki (wyłączny zapis) |
|---|---|---|
| [Oliwier] | `feat/rag-core` | `src/**`, `prompts/**`, `requirements.txt`, `.env.example`, `experiments/**` |
| [Ignacy] | `feat/data-eval` | `data/raw/**`, `data/manifest.csv`, `scripts/**`, `eval/**` |
| wspólne (PR) | `main` | `docs/**`, `CLAUDE.md`, `README.md`, `raport/**` |

Dziennik promptów: każda osoba pisze tylko we własnym pliku,
`raport/sections/prompty-oliwier.tex` (wpisy O1, O2, ...) albo
`raport/sections/prompty-ignacy.tex` (wpisy I1, I2, ...). Wspólny `prompty.tex` tylko je dołącza.

## Zadania

Statusy: `todo`, `w toku`, `gotowe`, `zablokowane`.

| ID | Właściciel | Zadanie | Pliki | Status |
|---|---|---|---|---|
| T-01 | [Oliwier] | Prototyp v0: ingest, chunking, indeks Chroma, tryby bez RAG / z RAG, UI Gradio | `src/**`, `requirements.txt`, `.env.example` | gotowe; wywołanie LLM do sprawdzenia po dodaniu klucza do `.env` |
| T-02 | [Oliwier] | Prompt v1 (bazowy) | `prompts/v1.md` | gotowe |
| T-03 | [Ignacy] | Pobranie 51 kart zajęć bloku AI zgodnie z kontraktem niżej, `data/manifest.csv` | `data/raw/**`, `data/manifest.csv`, `scripts/fetch_cards.py` | gotowe (2026-11-25: 51 kart, 0 błędów) |
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

**Pobieranie (uzgodnione w zespole 2026-11-25).** Skrypt `scripts/fetch_cards.py`
(biblioteka standardowa Pythona): pobiera publiczny plan bloku AI, wyciąga 51 linków do kart
i pobiera każdą kartę jeden raz, co 2,5 s (łącznie 52 zapytania). Już pobrane pliki pomija,
więc ponowne uruchomienie nie odpytuje serwera o te same karty. `krk.prz.edu.pl/robots.txt`
zawiera `Disallow: /`: świadomie pobieramy tylko tę listę stron publicznych, jednorazowo i
powoli, bez crawlera i bez stron za logowaniem. Ryzyko opisane w ADR-001 (ryzyko 6) i w
raporcie. Pozycje planu bez własnej karty (Język obcy, Zajęcia wybieralne I/II, Przedmiot
humanistyczno-społeczny I/II) prowadzą do innych planów i nie są pobierane.

```
python scripts/fetch_cards.py            # cały plan; --limit N dla próby
```

**Format.** Jeden plik = jedna karta zajęć. Preferowany oryginalny HTML
(`format=v1_html`). Dopuszczalne PDF z warstwą tekstową i DOCX. Bez skanów.

**Nazwa pliku.** Małe litery ASCII, bez spacji:
`inf1-ai_<mk>_<slug-nazwy>.html`, np. `inf1-ai_354_analiza-matematyczna-i-algebra-liniowa.html`.

**Manifest `data/manifest.csv`** (w gicie, bez danych osobowych), kolumny:

```
file,mk,course_name,semester,ects,source_url,retrieved_at,sha256
```

**Dane osobowe.** Karty w `data/raw/` są w repozytorium (decyzja zespołu 2026-11-25: pokazujemy
zbiór, na którym pracowaliśmy). To kopie publicznych stron uczelni, ale zawierają imiona i
nazwiska koordynatorów i prowadzących; nie wysyłamy ich w postaci surowej do zewnętrznych usług. Ingest (`src/ingest.py`) przed
indeksowaniem usuwa: blok od „Imię i nazwisko koordynatora” do następnego nagłówka sekcji
(koordynator i prowadzący w semestrach), adresy e-mail, numery telefonów. Do LLM trafiają
tylko fragmenty z indeksu. Po każdej zmianie zbioru: T-04 (ręczny przegląd próbki).

**Dane testowe.** `data/sample/` zawiera wyłącznie syntetyczne karty (fikcyjne treści
i osoby) do testu dymnego; ingest używa ich, gdy `data/raw/` jest pusty.
