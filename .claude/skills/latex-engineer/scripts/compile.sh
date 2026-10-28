#!/bin/bash

# LaTeX Engineer Smart Compiler
# Usage: ./compile.sh main.tex [clean]

FILE=$1
ACTION=$2

if [ -z "$FILE" ]; then
    echo "Usage: ./compile.sh <filename.tex> [clean]"
    exit 1
fi

# Base filename without extension
BASE=$(basename "$FILE" .tex)

clean_up() {
    echo "Cleaning auxiliary files..."
    rm -f *.aux *.log *.out *.toc *.bbl *.blg *.fdb_latexmk *.fls *.synctex.gz *.run.xml *.bcf
    echo "Done."
}

if [ "$ACTION" == "clean" ]; then
    clean_up
    exit 0
fi

if command -v latexmk &> /dev/null; then
    echo "Using latexmk for compilation..."
    latexmk -pdf -interaction=nonstopmode -shell-escape "$FILE"
else
    echo "latexmk not found, falling back to manual compilation..."
    pdflatex -interaction=nonstopmode -shell-escape "$FILE"
    bibtex "$BASE"
    pdflatex -interaction=nonstopmode -shell-escape "$FILE"
    pdflatex -interaction=nonstopmode -shell-escape "$FILE"
fi

if [ $? -eq 0 ]; then
    echo "----------------------------------------"
    echo "Compilation successful: ${BASE}.pdf created."
    echo "----------------------------------------"
else
    echo "----------------------------------------"
    echo "Compilation FAILED. Check ${BASE}.log for details."
    echo "----------------------------------------"
    exit 1
fi
