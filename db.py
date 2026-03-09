from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["travelgo"]

# Collections
users_collection = db["users"]
bookings_collection = db["bookings"]