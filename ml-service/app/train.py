import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load data
df = pd.read_csv("data/tickets.csv")

X = df["text"]
y = df["category"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vec, y)

# Save model + vectorizer
with open("models/model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model trained and saved")
