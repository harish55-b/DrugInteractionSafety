from db_connect import db, ddi_collection

sample_data = {
    "drug1": "aspirin",
    "drug2": "ibuprofen",
    "interaction": "Both are NSAIDs and can increase risk of GI bleeding",
    "safety": "Use With Caution",
    "mechanism": "Both inhibit COX enzymes leading to reduced prostaglandin synthesis",
    "side_effects": ["Stomach pain", "Nausea", "Bleeding risk"],
    "advice": "Avoid combining unless prescribed by a doctor",
    "provider": "Manual Entry"
}

ddi_collection.insert_one(sample_data)
print("✅ Test record added to MongoDB")
