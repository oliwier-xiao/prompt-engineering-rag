# The Engineer's Guide to LaTeX

Being a LaTeX Engineer means treating your document like a software project. This guide outlines the standards for code structure, technical writing, and advanced visualization.

## 1. Code Architecture

### File Separation
For any document over 10 pages, split it into multiple files.
- `main.tex`: Entry point. Only contains document class, `\input{preamble}`, `\begin{document}`, `\input{sections/...}`, and `\end{document}`.
- `preamble.tex`: Centralized package management and macro definitions.
- `sections/`: One `.tex` file per logical section.

### Clean Preamble
Group packages by function:
```latex
% --- Typography ---
\usepackage[T1]{fontenc}
\usepackage{microtype} % Better spacing/kerning

% --- Math ---
\usepackage{amsmath, amsfonts, amssymb}
\usepackage{mathtools}

% --- Figures & Tables ---
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
```

## 2. Professional Technical Writing (Anti-Slop)

AI assistants often generate "fluff". As an engineer, you must filter this out.

| AI Slop (Avoid) | Engineering Style (Use) |
| :--- | :--- |
| "This revolutionary approach provides..." | "The method achieves [X] accuracy..." |
| "In today's fast-paced world of technology..." | "Recent developments in [Field] have focused on..." |
| "It is important to note that..." | "Note that..." |
| "A significant amount of..." | "Approximately [Value]..." |

### Key Rules:
1. **Be Quantifiable**: Use numbers and data instead of vague adjectives (large, small, fast).
2. **Eliminate Redundancy**: If a sentence doesn't add new information, delete it.
3. **Consistency**: Use the same term for the same concept throughout the document.
4. **No Marketing Talk**: Avoid "innovative", "cutting-edge", "game-changing". Let the results speak for themselves.

## 3. Advanced Visualization

### Tables (booktabs)
- No vertical lines.
- Minimal horizontal lines (Top, Bottom, and Mid below headers).
- Align decimals in columns using `siunitx`.

### TikZ for Schematics
Avoid screenshots of PowerPoint diagrams. Use TikZ for crisp, vector-based schematics.
- Benefits: Font consistency, perfect scaling, version-controllable.
- Tip: Ask the AI for "TikZ code for a [System] diagram" rather than a generic image.

### pgfplots for Data
Plot your data directly in LaTeX.
```latex
\begin{tikzpicture}
\begin{axis}[xlabel=Time, ylabel=Value, grid=major]
  \addplot table [x=time, y=acc, col sep=comma] {data/results.csv};
\end{axis}
\end{tikzpicture}
```

## 4. Build Management

### latexmk
Stop running `pdflatex` multiple times manually. Use `latexmk`:
```bash
latexmk -pdf -pv main.tex
```
`-pv` opens the PDF viewer and updates it on every save.

### Version Control
- Add auxiliary files to `.gitignore` (`.aux`, `.log`, `.pdf`, `.toc`, `.bbl`, etc.).
- Use one sentence per line in your `.tex` files. This makes `git diff` much more readable.

## 5. Mathematical Rigor
- Use `\coloneqq` for definitions ($A \coloneqq B$).
- Use `\text{}` for text inside equations: $E_{\text{kinetic}} = \frac{1}{2}mv^2$.
- Use `cleveref` for references: `\cref{fig:result}` instead of `Figure \ref{fig:result}`.
