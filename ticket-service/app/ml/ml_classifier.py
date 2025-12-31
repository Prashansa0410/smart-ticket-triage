import pickle
import os
import numpy as np

# ---------------------------------------------------
# Load trained ML model
# ---------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as f:
    vectorizer, model = pickle.load(f)


# ---------------------------------------------------
# Hybrid Rule + ML + Confidence Threshold
# ---------------------------------------------------

def classify(text: str) -> dict:
    text_lower = text.lower()

    # -------- 1. RULE-BASED OVERRIDES (HIGH CONFIDENCE) --------
    if any(k in text_lower for k in ["payment", "debit", "credited", "refund", "upi"]):
        return {
            "category": "Payments",
            "priority": "High",
            "confidence": 1.0
        }

    if any(k in text_lower for k in ["login", "password", "otp", "authentication"]):
        return {
            "category": "Login",
            "priority": "Medium",
            "confidence": 1.0
        }

    # -------- 2. ML FALLBACK --------
    X = vectorizer.transform([text])

    predicted_category = model.predict(X)[0]

    # Get confidence score
    probabilities = model.predict_proba(X)[0]
    confidence = float(np.max(probabilities))

    # -------- 3. CONFIDENCE THRESHOLD --------
    if confidence < 0.6:
        return {
            "category": "Needs Review",
            "priority": "Low",
            "confidence": confidence
        }

    # -------- 4. PRIORITY DECISION --------
    if predicted_category in ["Payments", "Technical"]:
        priority = "High"
    else:
        priority = "Medium"

    return {
        "category": predicted_category,
        "priority": priority,
        "confidence": confidence
    }
