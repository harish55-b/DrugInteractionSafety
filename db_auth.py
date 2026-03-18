from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["drugsafe"]

# Select collection
users_collection = db["users"]