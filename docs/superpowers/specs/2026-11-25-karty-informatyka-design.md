# Pobranie i pocięcie kart zajęć Informatyki (WEII PRz)

Data: 2026-11-25. Obszar: Ignacy (dane, ingest). Status: do zatwierdzenia.

## Cel i dlaczego

Baza wiedzy asystenta RAG to karty zajęć z `krk.prz.edu.pl`. Na start pobieramy kierunek
Informatyka (WEII), cykl 2026. Później cały WEII, bez zmian w kodzie, bo zmieni się tylko lista
przedmiotów. Wynik to plik chunków, który ingest Oliwiera wczyta do wektorówki wybranej w ADR.

## Cele

- Jednorazowe, łagodne pobranie publicznych planów studiów Informatyki i kart zajęć, do których
  linkują (`karta.pl?mk=…&format=v1_html&C=`), do `data/raw/`.
- Pocięcie kart na chunki z metadanymi i anonimizacją prowadzących, zapis do
  `data/processed/chunks.jsonl`.
- Dwie strategie chunkingu: `headers` (bazowa) i `overlap` (eksperyment).

## Nie-cele

- Wybór wektorówki, embeddingów i ingestu do bazy (Oliwier, `docs/adr-001-stack.md`).
- Cokolwiek za logowaniem CAS. `ek.pl` to panel pracowników, a studenckie konto nie ma tam
  uprawnień (sprawdzone 2026-11-25).
- Osobne karty zajęć wybieralnych. Plan ma pozycje „Zajęcia wybieralne I/II” i pobieramy to, do
  czego linkują. Pełna lista przedmiotów do wyboru to osobny krok, jeśli będzie potrzebny.
- Inne kierunki WEII w tym kroku. `docs/dane.md` i `eval/questions.json` powstaną w następnym
  kroku, gdy dane będą na dysku.

## Anty-cele (porażka, nawet jeśli działa)

- Skrypt, który przy każdym uruchomieniu znowu odpytuje serwer uczelni.
- Imię i nazwisko prowadzącego w jakimkolwiek chunku.
- Cokolwiek z `data/raw/` lub `data/processed/` w gicie.

## Ograniczenia

- `robots.txt` serwisu: `Disallow: /`. Pobieramy wyłącznie publiczne strony: 1 listę planów
  kierunku, 14 planów i karty, do których linkują (rząd wielkości: kilkaset zapytań). Jedno
  zapytanie co ok. 2,5 s, z pominięciem już pobranych plików. Ryzyko opisujemy w raporcie
  (sekcja zagrożeń).
- Tylko biblioteka standardowa Pythona 3.11, bez nowych zależności. Kod w `scripts/`, nie w
  `src/` (blokada z `CLAUDE.md` do czasu ADR, uzgodnione z Ignacym).
- User-Agent ogólny (nazwa projektu studenckiego), bez danych osobowych.

## Podejścia

1. **Dwa kroki: `fetch_cards.py` i `parse_cards.py` (wybrane).** Serwer odpytujemy raz, a
   parser można uruchamiać offline dowolnie wiele razy. Surowe kopie z datą pobrania dają
   powtarzalność.
2. Jeden skrypt pobierający i tnący naraz. Każda zmiana chunkingu wymaga ponownego pobierania
   albo dopisania cache, czyli w praktyce wariantu 1. Odrzucone.
3. `requests`, BeautifulSoup, Scrapy. Odrzucone: nowe zależności przed ADR, a struktura kart
   jest prosta.

## Projekt

### Źródło listy przedmiotów: publiczny katalog planów (`plany.pl`)

Rozpoznane 2026-11-25, bez logowania:

```
plany.pl?lng=PL&TK=html&W=E                 → kierunki WEII (A, M, T, E, F; Informatyka = F)
plany.pl?lng=PL&TK=html&W=E&K=F             → 14 planów: forma × poziom × specjalność (S=70, 72, …)
plany.pl?lng=PL&TK=html&W=E&K=F&S=<id>      → tabela planu: semestr, jednostka, przedmiot,
                                              godziny W/C/L/P, ECTS, egzamin T/N, link do karty
```

Link do karty w planie: `http://krk.prz.edu.pl/karta.pl?mk=354&format=v1_html&C=`. Pusty `C`
(cykl) zostawiamy tak, jak podaje plan, a cykl odczytujemy z treści karty („Cykl kształcenia”).
Strony planu mają też linki `EFK=T` (efekty kierunkowe), które pomijamy.

### `scripts/fetch_cards.py`

- Parametry: `--faculty E`, `--program F` (kierunek; można podać kilka), `--delay 2.5`,
  `--out data/raw`, `--limit N` (próba na kilku kartach).
- Krok 1: pobiera listę planów kierunku, wyciąga identyfikatory `S` (bez linków `EFK=T`) i
  zapisuje każdy plan do `data/raw/plany/<K>_<S>.html`.
- Krok 2: z każdego planu wyciąga linki `karta.pl?…mk=(\d+)`, deduplikuje kody `mk` i pobiera
  karty do `data/raw/karty/<mk>.html`. Istniejący plik jest pomijany, więc kolejne uruchomienie
  nie odpytuje serwera ponownie.
- Indeks `data/raw/plany/index.jsonl`: dla każdego planu jego `S`, forma, poziom, specjalność
  (z nagłówka planu) i lista `mk`. Parser bierze stąd informację, w których planach występuje
  dany przedmiot.
- Walidacja odpowiedzi: HTTP 200, brak przekierowania na `cas.prz.edu.pl`. Dla karty w treści
  musi być „Karta zajęć” i `<h3>` z nazwą przedmiotu. Błąd jest logowany, a skrypt idzie dalej.
- Manifest `data/raw/manifest.jsonl`: `url`, `path`, `fetched_at`, `status`, `bytes`,
  `sha256`.

### `scripts/parse_cards.py`

- Wejście: `data/raw/karty/*.html`. Parser na `html.parser`.
- Struktura karty: 9 sekcji `<h4 id="item-1…9">`. W sekcji 1 pary
  `<span class="infoval">` + `<b>`, w pozostałych tabele z `<thead>` lub `<caption>`.
- Metadane karty (z sekcji 1): przedmiot (`<h3>`), cykl, wydział, kierunek, profil, poziom,
  forma, jednostka, status, język, `mk`. Pole „Formy zajęć” (`sem: 1 / W30 C45 / 6 ECTS / E`)
  rozbijane na semestr, godziny wg form, ECTS i formę zaliczenia.
- Czyszczenie: zdjęcie znaczników `<xsl-if>`, linków `javascript:getEfect` (zostaje sam kod
  KEK/PRK), pustych tabel i sekcji z „(-)”.
- Tabele do tekstu: wiersz jako „Nagłówek: wartość; …”. W sekcji 7 (oceny) wiersz ma postać
  „Ćwiczenia/Lektorat: <zasada>”, żeby forma zajęć nie odkleiła się od reguły.
- Anonimizacja (deterministyczna, po etykietach): wartości pól „Imię i nazwisko koordynatora”
  i `semestr N:` zamieniane na `[PROWADZĄCY]`. Zebrane nazwiska z tej karty są dodatkowo
  podmieniane w całym jej tekście. Regex łapie też e-maile (`[EMAIL]`) i telefony
  (`[TELEFON]`). Autorzy w literaturze zostają (publiczne dane bibliograficzne).
- Strategia `headers`: chunk = sekcja. Sekcja dłuższa niż `--max-chars` (domyślnie 2000) jest
  dzielona na granicach wierszy tabeli.
- Strategia `overlap`: okno po znakach (domyślnie 800, nakładka 200) w obrębie sekcji.
- Każdy chunk zaczyna się nagłówkiem kontekstu, np.
  `Przedmiot: Analiza matematyczna i algebra liniowa | Informatyka, I st., stacjonarne | sem. 1 | Sekcja: Sposób ustalania ocen cząstkowych i końcowej`.
- Rekord JSONL: `chunk_id` (`<mk>-item<N>[-<k>]`), `strategy`, `text`, `source_file`,
  `source_url` (z kotwicą `#item-N` do cytowania), `section`, `page` (`null`, bo HTML nie ma
  stron; pole zostaje dla zgodności ze wspólnym kontraktem chunka), metadane karty oraz
  `plans` (lista planów z `index.jsonl`, w których przedmiot występuje).
- Wyjście: `data/processed/chunks_<strategy>.jsonl`.
- Statystyki na wyjściu: liczba kart, chunków, min/mediana/max długości, karty z brakującymi
  sekcjami lub błędem parsowania, liczba podmian PII.

### Testy

`unittest` (biblioteka standardowa) na **syntetycznej** karcie w `tests/fixtures/` z
fikcyjnymi nazwiskami. Prawdziwa karta zawiera dane osobowe, więc nie trafia do repo.
Do tego syntetyczny fragment listy planów i jednego planu. Sprawdzają: wyciąganie `S` z listy
planów (bez `EFK=T`), wyciąganie `mk` z planu, metadane, rozbiór „Form zajęć”, brak nazwisk w
chunkach, tekst sekcji 7, obie strategie.

## Zostawione budującemu

Dokładne regexy, nazwy funkcji, format logów, obsługa ponowień po błędzie sieci (najwyżej jedna
próba więcej).
