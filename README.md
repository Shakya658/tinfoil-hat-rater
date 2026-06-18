# 🎩 Tinfoil Hat Rater

A satirical text-classification application that scores how strongly a claim resembles language patterns learned from false-labelled statements in the LIAR dataset.

Paste in a claim, receive a probability-style score, and get a deliberately theatrical verdict ranging from relatively ordinary language to full tinfoil.

## Important Interpretation

This application is **not a fact-checker**.

The model does not search evidence, verify sources, assess real-world events, or determine whether a statement is true. It only compares the wording of the input with linguistic patterns learned during training.

A carefully written false statement may receive a low score. A poorly phrased true statement may receive a high score.

## How It Works

1. The input text is transformed using TF-IDF.
2. A Logistic Regression classifier estimates similarity to the model's false-statement class.
3. The probability is converted into one of four satirical verdict levels.
4. Optional NewsAPI headlines can be loaded and scored using the same saved pipeline.

## Model Scope

| Component | Implementation |
|---|---|
| Dataset | LIAR benchmark dataset |
| Text representation | TF-IDF |
| Classifier | Logistic Regression |
| Saved artefact | `model/tinfoil_pipeline.pkl` |
| Interface | Streamlit |
| Optional external service | NewsAPI |

The committed pipeline contains both the text vectoriser and classifier, allowing raw text to be passed directly to `predict_proba()`.

## LIAR Dataset

The project uses the LIAR dataset introduced by William Yang Wang in 2017. It contains short political statements labelled by fact-checkers across multiple truthfulness categories.

The application simplifies the original labels into the classification target used by the training notebook. Because this is a modelling simplification, the score should be interpreted only as a portfolio demonstration of text classification.

## Score Bands

| Score | App verdict |
|---:|---|
| Below 25% | Agent of the System |
| 25% to below 50% | Suspicious Citizen |
| 50% to below 75% | Awakening |
| 75% and above | Full Tinfoil |

These bands are presentation rules, not independently validated factual-risk thresholds.

## Repository Structure

```text
tinfoil-hat-rater/
├── app.py
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── model/
│   └── tinfoil_pipeline.pkl
├── tests/
│   └── test_model_asset.py
└── notebooks/
    └── training notebook, when included
```

The saved model artefact is required to run the application. The notebook workflow is used to train and export that artefact.

## Run the Existing App

### 1. Clone the repository

```bash
git clone https://github.com/Shakya658/tinfoil-hat-rater.git
cd tinfoil-hat-rater
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate
```

### 3. Install application dependencies

```bash
pip install -r requirements.txt
```

### 4. Confirm the model exists

```text
model/tinfoil_pipeline.pkl
```

### 5. Launch Streamlit

```bash
streamlit run app.py
```

## Optional NewsAPI Setup

The app works without a NewsAPI key by displaying built-in example claims.

To enable live headlines, create:

```text
.streamlit/secrets.toml
```

Add:

```toml
NEWS_API_KEY = "your_api_key_here"
```

Do not commit the real key to GitHub.

When the API key is missing, invalid, rate-limited, or unavailable, the application falls back to its built-in examples.

## Development Environment

Install notebook and analysis dependencies with:

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` includes Jupyter, Notebook, Matplotlib and Seaborn in addition to the modelling libraries.

## Model Artefact Smoke Test

The repository includes a lightweight test that verifies:

- `model/tinfoil_pipeline.pkl` exists
- The saved pipeline loads successfully
- The pipeline exposes `predict_proba()`
- A sample input produces a two-class probability output
- The false-class probability is between 0 and 1

Run:

```bash
pip install pytest
pytest tests/test_model_asset.py
```

The test does not retrain or alter the model.

## Limitations

- The model analyses language patterns, not evidence.
- The LIAR dataset focuses on short political statements and does not represent all misinformation domains.
- Dataset labels reflect the original fact-checking process and the project's target transformation.
- A probability score is not a confidence-certified factual assessment.
- Live headline selection is based on keyword search, not confirmed misinformation.
- The application is satirical and intended for portfolio and educational use.

## Tech Stack

- Python
- Scikit-learn
- TF-IDF
- Logistic Regression
- Streamlit
- Joblib
- Requests
- NewsAPI integration

## Author

**Shirish Man Shakya**  
Data Analyst | Business Intelligence | Predictive Analytics

- [Portfolio](https://shakya658.github.io/portfolio/)
- [LinkedIn](https://linkedin.com/in/shirish-man-shakya)
- [GitHub](https://github.com/Shakya658)
