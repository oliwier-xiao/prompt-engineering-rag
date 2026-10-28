# Machine Learning Paper Writing for Engineers

Writing a paper for NeurIPS, ICML, or ICLR requires more than just good results; it requires a compelling technical narrative and strict adherence to formatting.

## 1. The Narrative Structure

A successful ML paper follows the "What, Why, So What" framework (Nanda et al.):
- **The What**: 1-3 novel claims.
- **The Why**: Rigorous evidence (empirical results, proofs).
- **The So What**: Why the community should care.

### Abstract (The 5-Sentence Formula)
1. **Achievement**: "We introduce [Method]..."
2. **Hardship/Importance**: "Existing methods fail because..."
3. **Approach**: "Our approach uses [Technique] to..."
4. **Evidence**: "We evaluate on [Datasets] and find..."
5. **Key Result**: "Specifically, we achieve a [Number]% improvement."

## 2. LaTeX Best Practices for ML

### Mathematical Notation
Standardize your notation. Most top conferences recommend using the notation from the "Deep Learning" book (Goodfellow et al.).
```latex
\usepackage{math_commands} % Often provided by conference templates
```

### Figures and Figures 1
Figure 1 is the most important figure. It should summarize the entire paper's contribution at a glance.
- Use vector graphics (PDF/EPS).
- Captions should be self-contained.

### Tables (Results)
- Bold the best results.
- Use `\pm` for standard deviation.
- Clearly state the number of seeds used.

## 3. Mandatory Sections

### Limitations
Modern conferences (NeurIPS, ICLR, ACL) require a dedicated Limitations section. Be honest about where your method fails.

### Ethics Statement / Broader Impact
Mandatory for ICML and NeurIPS. Discuss potential societal consequences (bias, energy usage, etc.).

## 4. Citation Integrity

**Hallucinated citations are a grounds for immediate rejection.**
- Fetch BibTeX programmatically.
- Use `\citep` for parenthetical citations and `\citet` for narrative citations.
- Check if "Under Review" papers have been published before your submission.

## 5. Page Limits & Formatting

| Conference | Page Limit (Main) | Extra (Camera-Ready) |
| :--- | :--- | :--- |
| NeurIPS | 9 pages | 0 |
| ICML | 8 pages | +1 |
| ICLR | 9 pages | +1 |

- **Don't tweak margins**: Reviewers notice and it's grounds for desk rejection.
- **Appendices**: Move proofs and hyperparameter tables to the appendix. References do not count towards the page limit.
