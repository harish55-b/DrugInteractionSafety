# db_config.py
from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access main database
db = client["drug_ai"]

# Collections
ddi_collection = db["ddi_predictions"]
drug_info_collection = db["drug_info"]

print("✅ MongoDB connected: drug_ai database active.")
