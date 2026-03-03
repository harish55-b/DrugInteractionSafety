import json
import random

classes = [
    "NSAID", "Analgesic", "Antibiotic", "Anticoagulant", "Antidiabetic",
    "Antihypertensive", "Antidepressant", "Antifungal", "Antiviral",
    "Statin", "ACE Inhibitor", "Beta Blocker"
]

uses = [
    "Pain relief", "Fever reduction", "Inflammation control",
    "Blood pressure control", "Blood sugar control",
    "Infection treatment", "Cholesterol reduction",
    "Clot prevention", "Mental health treatment"
]

side_effects = [
    "Nausea", "Vomiting", "Headache", "Dizziness",
    "Rash", "Fatigue", "Diarrhea", "Bleeding"
]

warnings = [
    "Avoid alcohol",
    "Use with caution in pregnancy",
    "Monitor liver function",
    "Monitor kidney function",
    "Risk of bleeding",
    "May cause drowsiness"
]

drugs = []

for i in range(1, 201):
    drug = {
        "drug_name": f"drug_{i}",
        "generic_name": f"generic_{i}",
        "class": random.choice(classes),
        "uses": random.sample(uses, 2),
        "common_side_effects": random.sample(side_effects, 2),
        "warnings": random.sample(warnings, 2),
        "pregnancy_category": random.choice(["A", "B", "C", "D"]),
        "metabolism": random.choice(["Liver", "Kidney", "Liver (CYP450)"]),
        "excretion": random.choice(["Urine", "Bile"]),
        "source": "synthetic_openfda_style"
    }
    drugs.append(drug)

with open("drug_info_200.json", "w") as f:
    json.dump(drugs, f, indent=2)

print("✅ drug_info_200.json created with 200 drugs")
