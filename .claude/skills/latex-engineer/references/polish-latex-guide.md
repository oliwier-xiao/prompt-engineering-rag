# Przewodnik Inżyniera po Polskim LaTeXu

Pisanie dokumentacji technicznej i prac naukowych w języku polskim w systemie LaTeX wymaga znajomości kilku specyficznych ustawień i pakietów, aby wynik końcowy był zgodny z polskimi normami typograficznymi.

## 1. Niezbędna Konfiguracja

Podstawowy zestaw pakietów dla języka polskiego:

```latex
\usepackage[T1]{fontenc}        % Kodowanie czcionki (obsługa ogonków)
\usepackage[utf8]{inputenc}    % Kodowanie znaków w pliku źródłowym
\usepackage[polish]{babel}     % Polskie nazwy sekcji (np. "Spis treści")
\usepackage{polski}            % Dodatkowe makra i formatowanie dla PL
```

## 2. Polskie Znaki i Typografia

### Cudzysłowy
W języku polskim używamy cudzysłowów dolnych na początku i górnych na końcu:
- Prawidłowo: `,,tekst''`
- Nieprawidłowo: `"tekst"` (użycie standardowego cudzysłowu z klawiatury da dwa górne)

### Myślniki i Pauzy
- **Pauza (`---`)**: Używana jako myślnik w tekście. W polskiej tradycji często otoczona cienkimi spacjami.
- **Półpauza (`--`)**: Używana w zakresach (np. 10--20 m) oraz jako myślnik (alternatywa dla pauzy).

### Sierotki (Jednoliterowe spójniki)
Zgodnie z polskimi zasadami, spójniki jednoliterowe (*a, i, o, u, w, z*) nie powinny zostawać na końcu linii.
- Rozwiązanie ręczne: Używaj twardej spacji `~`, np. `w~domu`, `i~wtedy`.
- Rozwiązanie automatyczne: Użyj pakietu `enunumerate` lub skryptów typu `tex-unclutter`. Najprościej w LaTeXu: `\usepackage{indentfirst}` pomaga w strukturze, ale nie rozwiązuje sierotek. Można użyć skryptu `perl -pi -e 's/ ([aiouzw]) / $1~ /g' plik.tex`.

## 3. Formatowanie Dat i Liczb

### Daty
Pakiet `polski` lub `babel` poprawnie formatuje daty przez `\today`. Jeśli potrzebujesz specyficznego formatu:
```latex
\usepackage{datetime2}
\DTMsetdatestyle{dd.mm.yyyy}
```

### Liczby i Jednostki
W Polsce separatorem dziesiętnym jest **przecinek**, a nie kropka.
Pakiet `siunitx` pozwala na automatyczną zamianę:
```latex
\usepackage{siunitx}
\sisetup{output-decimal-marker = {,}}

% Użycie:
\num{3.14} % Wynik: 3,14
\qty{10}{\meter\per\second}
```

## 4. Bibliografia w języku polskim

Przy użyciu `biblatex`, ustaw język dokumentu:
```latex
\usepackage[style=numeric,language=polish]{biblatex}
```
Dzięki temu skróty takie jak "red.", "wyd.", "t." będą w języku polskim.

## 5. Przykładowy Szablon PL

```latex
\documentclass[12pt,a4paper]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[polish]{babel}
\usepackage{polski}
\usepackage{indentfirst}
\usepackage{geometry}
\geometry{margin=2.5cm}

\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}

\title{Tytuł Dokumentu}
\author{Inżynier Anonim}
\date{\today}

\begin{document}

\maketitle

\tableofcontents

\section{Wstęp}
To jest przykładowy tekst w~języku polskim. Pamiętamy o~twardych spacjach po spójnikach oraz o~poprawnych cudzysłowach: ,,tak to się robi''.

\section{Metodyka}
Używamy jednostek SI: \num{10.5} m/s.

\end{document}
```
