import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


# Training dataset
data = [
    # Network connectivity
    ("wifi is not working", "Network connectivity", "Medium"),
    ("internet connection is very slow", "Network connectivity", "Medium"),
    ("cannot connect to office network", "Network connectivity", "High"),
    ("network is disconnected", "Network connectivity", "High"),
    ("internet is unavailable for everyone", "Network connectivity", "Critical"),
    ("network connection keeps dropping", "Network connectivity", "Medium"),
    ("LAN cable is not connecting", "Network connectivity", "Low"),
    ("network outage in office", "Network connectivity", "Critical"),

    # Software installation
    ("install python software", "Software installation", "Low"),
    ("need installation of office software", "Software installation", "Low"),
    ("application installation failed", "Software installation", "Medium"),
    ("software is not installing", "Software installation", "Medium"),
    ("install antivirus on laptop", "Software installation", "Low"),
    ("need software installation urgently", "Software installation", "High"),
    ("application setup problem", "Software installation", "Medium"),
    ("installation error appears", "Software installation", "Medium"),

    # Password reset
    ("forgot my password", "Password reset", "Low"),
    ("reset my account password", "Password reset", "Low"),
    ("unable to login due to password", "Password reset", "Medium"),
    ("password expired", "Password reset", "Low"),
    ("account is locked", "Password reset", "High"),
    ("login password is not accepted", "Password reset", "Medium"),
    ("cannot access my account", "Password reset", "Medium"),
    ("need urgent password reset", "Password reset", "High"),

    # VPN access
    ("vpn is not connecting", "VPN access", "Medium"),
    ("unable to access vpn", "VPN access", "Medium"),
    ("vpn connection failed", "VPN access", "Medium"),
    ("vpn access needed for remote work", "VPN access", "Low"),
    ("vpn disconnected frequently", "VPN access", "Medium"),
    ("vpn unavailable for the entire team", "VPN access", "Critical"),
    ("remote vpn login issue", "VPN access", "Medium"),
    ("vpn authentication error", "VPN access", "High"),

    # Hardware problems
    ("laptop screen is broken", "Hardware problems", "High"),
    ("keyboard is not working", "Hardware problems", "Medium"),
    ("computer is not turning on", "Hardware problems", "High"),
    ("printer is not working", "Hardware problems", "Medium"),
    ("hard disk failure", "Hardware problems", "Critical"),
    ("mouse is damaged", "Hardware problems", "Low"),
    ("laptop battery issue", "Hardware problems", "Medium"),
    ("computer overheating", "Hardware problems", "High"),

    # System troubleshooting
    ("computer is running slowly", "System troubleshooting", "Medium"),
    ("system keeps freezing", "System troubleshooting", "High"),
    ("windows error appeared", "System troubleshooting", "Medium"),
    ("blue screen error", "System troubleshooting", "High"),
    ("computer restart problem", "System troubleshooting", "Medium"),
    ("system crashes repeatedly", "System troubleshooting", "High"),
    ("application is not responding", "System troubleshooting", "Medium"),
    ("system failure affecting work", "System troubleshooting", "Critical"),

    # Additional severity training examples
    ("minor display issue", "System troubleshooting", "Low"),
    ("slow computer performance", "System troubleshooting", "Medium"),
    ("complete system failure", "System troubleshooting", "Critical"),
    ("urgent network failure", "Network connectivity", "Critical"),
    ("small software error", "Software installation", "Low"),
    ("all users cannot login", "Password reset", "Critical"),
    ("urgent hardware failure", "Hardware problems", "Critical"),
    ("vpn failure affecting team", "VPN access", "Critical"),

        # UI customization
    ("change dashboard color theme", "UI customization", "Low"),
    ("I want to change the color theme of my dashboard", "UI customization", "Low"),
    ("customize dashboard appearance", "UI customization", "Low"),
    ("change background color", "UI customization", "Low"),
    ("dark mode is not available", "UI customization", "Low"),
    ("change font size in dashboard", "UI customization", "Low"),
    ("dashboard layout customization", "UI customization", "Low"),
    ("modify dashboard design", "UI customization", "Low"),

    # Billing problems
    ("charged twice for my subscription", "Billing problems", "High"),
    ("incorrect billing amount", "Billing problems", "Medium"),
    ("payment failed", "Billing problems", "Medium"),
    ("refund not received", "Billing problems", "Medium"),
    ("billing error on my account", "Billing problems", "Medium"),
    ("unauthorized payment from my account", "Billing problems", "High"),

    # Email problems
    ("unable to send email", "Email problems", "Medium"),
    ("emails are not received", "Email problems", "Medium"),
    ("email server is down", "Email problems", "Critical"),
    ("outlook is not opening", "Email problems", "Medium"),
    ("email account is locked", "Email problems", "High"),
    ("email delivery failed", "Email problems", "Medium"),

    # Access permissions
    ("request access to shared folder", "Access permissions", "Low"),
    ("permission denied when opening file", "Access permissions", "Medium"),
    ("need access to company portal", "Access permissions", "Low"),
    ("unauthorized access to application", "Access permissions", "High"),
    ("employee cannot access shared files", "Access permissions", "Medium"),

    # Application bugs
    ("application has a bug", "Application bugs", "Medium"),
    ("website displays incorrect information", "Application bugs", "Medium"),
    ("application crashes when opened", "Application bugs", "High"),
    ("error occurs while submitting form", "Application bugs", "Medium"),
    ("software bug affecting all employees", "Application bugs", "Critical"),
    ("button is not working on the website", "Application bugs", "Low"),
]

texts = [item[0] for item in data]
categories = [item[1] for item in data]
severities = [item[2] for item in data]


# Category model
category_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

category_model.fit(texts, categories)


# Severity model
severity_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

severity_model.fit(texts, severities)


# Save both models
os.makedirs("models", exist_ok=True)

with open("models/ticket_classifier.pkl", "wb") as file:
    pickle.dump({
        "category_model": category_model,
        "severity_model": severity_model
    }, file)

print("AI models trained and saved successfully!")