from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create or access the database
db = client["drug_ai"]

# Define collections
ddi_collection = db["ddi_predictions"]
drug_info_collection = db["drug_info"]

print("✅ Connected to MongoDB successfully!")
