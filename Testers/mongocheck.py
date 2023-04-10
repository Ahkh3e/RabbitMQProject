from pymongo import MongoClient

# Connect to the MongoDB instance
client = MongoClient('mongodb://admin:secret@localhost:27017/')

# Set the database and collection names
db = client['project']
patients_collection = db['users']

# Query the patients collection to get all documents
patients = patients_collection.find()

# Print each patient document
for patient in patients:
    print(patient)