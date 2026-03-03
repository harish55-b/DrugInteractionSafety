# ==========================================================
# DRUG–DRUG INTERACTION CHECKER
# Groq (Primary) + Classifier (Fallback)
# ==========================================================

from ai_provider_manager import analyze_drug_interaction
from ddi_classifier import DDIClassifier

classifier = DDIClassifier()

def check_ddi(drug1, drug2):

    # 🔹 Step 1: Try Groq AI
    ai_result = analyze_drug_interaction(drug1, drug2)

    # If Groq worked successfully
    if ai_result.get("provider") == "Groq":
        return ai_result

    # 🔹 Step 2: If Groq failed → Use Classifier
    print("⚠️ Groq failed. Using Classifier fallback.")
    clf_result = classifier.predict_interaction(drug1, drug2)

    return clf_result