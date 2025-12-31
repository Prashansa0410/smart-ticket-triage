import pickle

# Load model
with open("models/model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)


def classify_ticket(text: str):
    X = vectorizer.transform([text])
    category = model.predict(X)[0]

    # Simple rule for priority
    if category == "Payments":
        priority = "High"
    else:
        priority = "Medium"

    return {
        "category": category,
        "priority": priority
    }
