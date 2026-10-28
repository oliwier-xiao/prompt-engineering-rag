# Designing Scientific Posters in LaTeX

A research poster is a visual aid for a conversation, not a paper pasted on a wall.

## 1. Visual Hierarchy

1.  **Title**: Visible from 5 meters (min 72pt).
2.  **Headings**: Clear and bold (min 36pt).
3.  **Body Text**: Readable from 1.5 meters (min 24pt).
4.  **White Space**: 40-50% of the poster should be empty. Avoid "Wall of Text".

## 2. LaTeX Packages for Posters

### tikzposter (Recommended)
Modern, flexible, and easy to use.
```latex
\documentclass[25pt, a0paper, portrait]{tikzposter}
\title{Poster Title}
\author{Author Name}
\institute{Institute Name}
\usetheme{Simple}

\begin{document}
\maketitle
\begin{columns}
  \column{0.5}
  \block{Introduction}{Text goes here...}
  \column{0.5}
  \block{Results}{Figures go here...}
\end{columns}
\end{document}
```

### beamerposter
Good for reusing content from Beamer presentations. Uses standard Beamer columns and blocks.

### baposter
Great for modular layouts with boxes that have specific placements.

## 3. Visual Element Guidelines

- **Graphics**: 60-70% of the area should be visual (figures, charts, diagrams).
- **Text**: Maximum 800 words for the whole poster.
- **Figures**: Use high-resolution or vector graphics. Label everything clearly.
- **QR Codes**: Include a QR code linking to the full paper or repository.

## 4. Color and Typography

- **Contrast**: Use high contrast (Black on White or Dark Blue on White).
- **Colorblind Safety**: Use palettes like Okabe-Ito or Paul Tol.
- **Consistency**: Match the colors in your plots with the poster theme colors.

## 5. Standard Sizes

- **A0**: 841 x 1189 mm (33.1 x 46.8 in) - Most common.
- **A1**: 594 x 841 mm (23.4 x 33.1 in).
- **US Standard**: 36 x 48 inches.
- **NeurIPS/ICML**: Check specific annual requirements.
