from pathlib import Path

import joblib


MODEL_PATH = Path("model/tinfoil_pipeline.pkl")


def test_pipeline_exists_loads_and_predicts_probability():
    assert MODEL_PATH.exists(), f"Missing model artefact: {MODEL_PATH}"

    pipeline = joblib.load(MODEL_PATH)

    assert hasattr(pipeline, "predict_proba"), "Saved pipeline must expose predict_proba"

    probabilities = pipeline.predict_proba(["A sample claim for smoke testing."])

    assert probabilities.shape == (1, 2)
    assert 0 <= probabilities[0][1] <= 1
