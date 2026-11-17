
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("dataset.csv")

# Separate input and output
X = data.drop("label", axis=1)
y = data["label"]

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained successfully!")
print("Model saved as model.pkl")
