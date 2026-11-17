
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import ipaddress
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

suspicious_words = [
    "login", "verify", "account", "password",
    "secure", "update", "free", "bonus",
    "claim", "bank", "confirm", "signin"
]

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    try:
        ipaddress.ip_address(hostname)
        ip_flag = 1
    except ValueError:
        ip_flag = 0

    return [[
        len(url),
        1 if parsed.scheme == "https" else 0,
        url.count("."),
        url.count("-"),
        url.count("@"),
        ip_flag,
        sum(word in url.lower() for word in suspicious_words)
    ]]

@app.route("/")
def home():
    return "Improved Scam Website Detection Backend Running!"

@app.route("/check", methods=["POST"])
def check_website():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL"}), 400

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Enter a URL starting with http:// or https://"}), 400

    features = extract_features(url)
    prediction = int(model.predict(features)[0])

    return jsonify({
        "url": url,
        "result": "SCAM" if prediction == 1 else "SAFE",
        "warning": "ML prediction only; not a safety guarantee"
    })

if __name__ == "__main__":
    app.run(debug=True)
