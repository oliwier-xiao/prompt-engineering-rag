# Uczelniany Asystent Sylabusów i Zasad Zaliczeń (RAG)

Projekt na laboratorium **Prompt Engineering**, temat 12: *Asystent analizy dokumentów typu RAG*
(poziom zaawansowany, ocena bazowa 5,0).

Asystent odpowiada na pytania studentów o zasady zaliczenia **wyłącznie na podstawie wgranych
sylabusów i regulaminów**, cytuje dokument źródłowy i odmawia odpowiedzi, gdy informacji w
dokumentach nie ma.

> Status: **inicjalizacja**. Wybrany temat, zakres i plan pracy. Stack (UI, model, wektorówka)
> zostanie zatwierdzony w następnym etapie po porównaniu Gradio, Streamlit i Chainlit.

## Cel

Pokazać różnicę między „nagim” LLM-em a modelem uziemionym w kontekście (RAG):

| | Bez RAG | Z RAG |
|---|---|---|
| Pytanie o próg obecności | Ogólnikowa „typowa” norma uczelni | Wartość z konkretnego sylabusa, z cytatem |
| Pytanie o przedmiot spoza bazy | Zgaduje na podstawie wiedzy ogólnej | Odmawia: informacji nie ma w dostarczonych dokumentach |
| Pytanie o szczegół, którego sylabus nie precyzuje | Dopowiada „akademickie” wymówki | Wskazuje brak danych i odsyła do prowadzącego |

## Zakres minimalny (wymóg zaliczeniowy)

1. Przetwarzanie dokumentów (PDF/DOCX sylabusów wybranego kierunku).
2. Fragmentacja (chunking), np. po nagłówkach.
3. Wyszukiwanie kontekstu.
4. Odpowiedzi ze wskazaniem źródeł i ograniczeniem halucynacji.
5. Porównanie odpowiedzi **bez RAG i z RAG**.
6. Min. 3 istotnie różne wersje kluczowego promptu, analiza nieudanych wyników, omówienie ryzyk
   (etyka, prawo, prywatność, bezpieczeństwo), informacja o modelach, ustawieniach i
   ograniczeniach odtwarzalności.

Szczegóły i kryteria oceny: [`docs/wymagania.md`](docs/wymagania.md).
Pełny opis pomysłu i decyzji: [`docs/projekt.md`](docs/projekt.md).

## Struktura repozytorium

```
.
├── README.md             ten plik
├── CLAUDE.md             instrukcje dla agenta (m.in. obowiązkowy dziennik promptów)
├── .claude/              wspólna konfiguracja Claude Code (bez współautorstwa w commitach)
│   └── skills/latex-engineer/   skill do pracy z LaTeX-em (dla całego zespołu)
├── docs/                 wymagania, opis projektu, decyzje (ADR), plan pracy
├── data/
│   ├── raw/              źródłowe sylabusy (poza gitem, patrz licencje)
│   └── processed/        wynik ekstrakcji i chunkingu (poza gitem)
├── src/                  kod aplikacji RAG (po zatwierdzeniu stacku)
├── prompts/              wersje promptów systemowych (v1, v2, v3 ...) jako pliki
├── eval/                 zestaw pytań testowych (z odpowiedzią i pułapki odmowy)
├── experiments/          logi uruchomień i wyniki porównań (bez RAG / z RAG)
└── raport/               raport końcowy w LaTeX
    ├── main.tex
    ├── preamble.tex
    ├── sections/         rozdziały raportu + prompty.tex (dziennik promptów)
    ├── figures/
    └── bib/
```

## Raport (LaTeX)

```bash
cd raport
latexmk -pdf -outdir=build main.tex     # PDF w raport/build/main.pdf
latexmk -C -outdir=build                # sprzątanie
```

Wymaga TeX Live z pakietami `babel-polish`, `listings`, `booktabs`, `biblatex`.
Pliki `.tex` powstają według skilla `latex-engineer` (`.claude/skills/latex-engineer/`), który
Claude Code ładuje automatycznie po sklonowaniu repo.
Dziennik promptów użytych z modelem (z modelem i effortem) prowadzimy na bieżąco w
[`raport/sections/prompty.tex`](raport/sections/prompty.tex), zasady w [`CLAUDE.md`](CLAUDE.md).

## Plan pracy

Zgodny z przebiegiem zajęć: start, planowanie, prototypowanie, iteracja, finalizacja, zaliczenie.
Rozpisany w [`docs/plan.md`](docs/plan.md).

## Użycie GenAI

Projekt powstaje z udziałem modeli generatywnych. Zgodnie z zasadami przedmiotu dokumentujemy
prompty, iteracje, modele i ustawienia (`raport/sections/prompty.tex`), a treści wygenerowane lub
istotnie przekształcone przez AI oznaczamy w raporcie. Wyniki weryfikuje zespół.

## Licencja

Do ustalenia (dane źródłowe: sylabusy uczelni, sprawdzić warunki użycia przed publikacją).
