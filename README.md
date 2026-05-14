# 🎩 Tinfoil Hat Rater

A satirical conspiracy theory plausibility scorer. Paste in a claim, get a verdict.

Built with the LIAR dataset (12,791 statements rated by PolitiFact fact-checkers) and a TF-IDF + Logistic Regression pipeline. It detects the **language patterns** of misinformation — not whether something is actually true.

A well-worded lie can score low. A clumsily worded truth can score high. That's the point.

---

## How It Works

1. Your claim gets converted into a numerical representation using TF-IDF
2. A logistic regression model scores how closely the language resembles statements that were labelled false by professional fact-checkers
3. You get a verdict — from *Agent of the System* to *Full Tinfoil*

---

## Stack

- Python, scikit-learn, Streamlit
- LIAR Dataset — Wang, W.Y. (2017), UCSB
- News API for live conspiracy-adjacent headlines

---

## Disclaimer

This is a style detector, not a fact-checker. The model doesn't know what's true. Neither do most people on the internet.