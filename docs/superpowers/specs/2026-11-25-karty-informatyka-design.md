# Pobranie kart zajęć bloku AI (Informatyka, WEII PRz)

Data: 2026-11-25. Obszar: Ignacy (dane). Status: **zrealizowane** (T-03 w `docs/tasks.md`).

## Cel i dlaczego

Baza wiedzy asystenta RAG to karty zajęć z `krk.prz.edu.pl`. Zakres zgodny z ADR-001 i
kontraktem w `docs/tasks.md`: Informatyka, I stopień, stacjonarne, blok tematyczny AI, cykl
2026/2027, 51 kart. Parsowanie, chunking, usuwanie danych osobowych i indeksowanie robi
`src/ingest.py` (Oliwier). Ten dokument opisuje tylko pozyskanie danych.

## Cele

- Pobrać 51 kart z publicznego planu studiów do `data/raw/` (poza gitem), z nazwami
  `inf1-ai_<mk>_<slug>.html`.
- Utworzyć `data/manifest.csv` (w gicie, bez danych osobowych):
  `file,mk,course_name,semester,ects,source_url,retrieved_at,sha256`.

## Nie-cele

- Parsowanie i chunking (`src/ingest.py`, Docling).
- Inne kierunki i bloki WEII. Skrypt przyjmie inny plan przez `--plan-url` i `--prefix`, ale
  zakres zmienia się tylko przez zmianę kontraktu w `docs/tasks.md`.
- Strony za logowaniem CAS. `ek.pl` to panel pracowników; konto studenckie nie ma tam uprawnień.
- Pozycje planu bez własnej karty (Język obcy, Zajęcia wybieralne I/II, Przedmiot
  humanistyczno-społeczny I/II); linkują do innych planów.

## Anty-cele

- Ponowne odpytywanie serwera przy każdym uruchomieniu.
- Surowe karty (z nazwiskami prowadzących) w gicie lub w zewnętrznych usługach.

## Ograniczenia

- `robots.txt` serwisu: `Disallow: /`. Decyzja zespołu: pobieramy tylko 52 publiczne strony
  (plan i 51 kart), jednorazowo, co 2,5 s. Ryzyko w ADR-001 (ryzyko 6) i w raporcie.
- Tylko biblioteka standardowa Pythona, bez nowych zależności.
- User-Agent ogólny (projekt studencki), bez danych osobowych.

## Rozpoznanie serwisu

```
plany.pl?lng=PL&TK=html&W=E               → kierunki WEII (A, M, T, E, F; Informatyka = F)
plany.pl?lng=PL&TK=html&W=E&K=F           → 14 planów: forma × poziom × specjalność
plany.pl?lng=PL&W=E&K=F&…&S=2424&…&O=T    → plan bloku AI: semestr, przedmiot, godziny, ECTS,
                                            egzamin i link karta.pl?mk=<mk>&format=v1_html&C=
```

- `mk` = „Kod zajęć” z karty.
- Pusty `C` daje bieżący cykl. Karta `mk=354` z `C=` i z `C=2026` jest identyczna (SHA-256).
- Karta ma 9 sekcji `<h4 id="item-1…9">`. Nazwiska koordynatora i prowadzących są tylko w
  sekcji 1, pod etykietami „Imię i nazwisko koordynatora” i „semestr N:”.

## Podejścia

1. **Skrypt pobierający z listy w planie (wybrane).** Powtarzalne, z manifestem i sumami
   kontrolnymi. Obciążenie serwera takie samo jak przy ręcznym zapisaniu tych samych stron.
2. Ręczne zapisanie 51 stron z przeglądarki (pierwotny kontrakt). Ta sama liczba zapytań,
   ale więcej pracy i ryzyko pomyłek w nazwach plików i manifeście.
3. Crawler całego serwisu lub enumeracja kolejnych `mk`. Odrzucone: tysiące zapytań, wbrew
   `robots.txt`.

## Realizacja: `scripts/fetch_cards.py`

- Pobiera plan (`--plan-url`, domyślnie blok AI), wyciąga z wierszy tabeli: semestr, `mk`,
  nazwę przedmiotu, ECTS. Karta w kilku semestrach ma w manifeście wartości po średniku
  (np. Seminarium dyplomowe `6;7`).
- Pobiera każdą kartę raz (`--delay 2.5`), pomija istniejące pliki, `--limit N` do prób.
- Walidacja: HTTP 200, brak przekierowania na `cas.prz.edu.pl`, w treści „Karta zajęć” i `<h3>`.
- Nazwa pliku: `<prefix>_<mk>_<slug>.html`, slug ASCII z nazwy przedmiotu.
- Manifest jest scalany po `mk` i sortowany.

## Wynik (2026-11-25)

51 kart, 0 błędów, `data/manifest.csv` z 51 wierszami. Każda karta zawiera „Karta zajęć” i
kierunek Informatyka.

## Uwagi dla ingestu (`src/ingest.py`, Oliwier)

- Sekcja 7 „Sposób ustalania ocen” to tabela „forma zajęć → zasada”. Dobrze, gdy chunk trzyma
  formę zajęć razem z regułą (np. „Ćwiczenia: …”).
- W „Treściach programowych” są znaczniki `<xsl-if>`, a przy efektach linki
  `javascript:getEfect`. Warto je usunąć przed indeksowaniem.
- Pole „Formy zajęć” (`sem: 1 / W30 C45 / 6 ECTS / E`) nadaje się na metadane (semestr, ECTS,
  egzamin).
