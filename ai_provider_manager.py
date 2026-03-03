# ==========================================================
# AI PROVIDER MANAGER (FINAL CLEAN VERSION)
# Groq Only – No Ollama – Production Ready
# ==========================================================

import os
import json
import re
import requests
from dotenv import load_dotenv

# ==========================================================
# 🔐 Load API Key
# ==========================================================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================================
# 🧠 Prompt Builder for Drug–Drug Interaction
# ==========================================================
def build_prompt(drug1, drug2):
    return f"""
You are a pharmacology AI assistant.

Analyze the interaction between:
1. {drug1}
2. {drug2}

Return ONLY valid JSON in this format:

{{
  "interaction": "{drug1} + {drug2}",
  "safety": "Safe | Use With Caution | Unsafe | Unsafe at High Dose",
  "mechanism": "Detailed explanation of interaction mechanism",
  "side_effects": ["side effect 1", "side effect 2"],
  "advice": "Short patient-friendly advice"
}}
""".strip()


# ==========================================================
# 🧹 Extract JSON from AI Output
# ==========================================================
def extract_json(text):
    text = text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None


# ==========================================================
# ⚙️ GROQ CALL (Primary & Only AI)
# ==========================================================
def call_groq(drug1, drug2):

    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY in .env file")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a pharmacology AI that ALWAYS returns valid JSON only."
            },
            {
                "role": "user",
                "content": build_prompt(drug1, drug2)
            },
        ],
        "temperature": 0.3,
        "max_tokens": 700,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API error {response.status_code}: {response.text}")

    text = response.json()["choices"][0]["message"]["content"]

    parsed = extract_json(text)

    if not parsed:
        raise RuntimeError("Groq returned invalid JSON format")

    parsed["provider"] = "Groq"
    return parsed


# ==========================================================
# 🔁 Main Analyze Function (Groq Only)
# ==========================================================
def analyze_drug_interaction(drug1, drug2):
    try:
        return call_groq(drug1, drug2)
    except Exception as e:
        return {
            "interaction": f"{drug1} + {drug2}",
            "safety": "Unknown",
            "mechanism": f"AI service unavailable: {str(e)}",
            "side_effects": [],
            "advice": "Consult healthcare provider.",
            "provider": "None"
        }