import os
import pickle

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "ticket_classifier.pkl")


def load_model():
    with open(MODEL_PATH, "rb") as file:
        models = pickle.load(file)

    return models


models = load_model()

# Keyword rules: words that clearly show how serious a ticket is
LOW_WORDS = ["no rush", "not urgent", "minor", "whenever", "low priority", "no hurry"]
CRITICAL_WORDS = ["everyone", "entire", "whole office", "whole team", "all users",
                  "outage", "company wide", "company-wide", "production down", "server down"]
HIGH_WORDS = ["urgent", "urgently", "asap", "immediately", "critical", "deadline",
              "client meeting", "blocking", "cannot work", "emergency"]


def apply_severity_rules(description, model_severity):
    text = description.lower()
    if any(w in text for w in LOW_WORDS):
        return "Low"
    if any(w in text for w in CRITICAL_WORDS):
        return "Critical"
    if any(w in text for w in HIGH_WORDS):
        return "High"
    return model_severity


def classify_ticket(description):

    category_model = models["category_model"]
    severity_model = models["severity_model"]

    category = category_model.predict([description])[0]
    severity = severity_model.predict([description])[0]
    severity = apply_severity_rules(description, severity)

    # Priority assignment
    priority_map = {
        "Critical": "P1 - Urgent",
        "High": "P2 - High",
        "Medium": "P3 - Medium",
        "Low": "P4 - Low"
    }

    priority = priority_map.get(severity, "P3 - Medium")

    return category, severity, priority