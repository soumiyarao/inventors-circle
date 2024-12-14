import json
import random
from pymongo import MongoClient

with open("ds_patent_dataset.json", "r") as file:
    dataset = json.load(file)

def to_sentence_case(name):
    name_parts = name.split()
    capitalized_name_parts = [part.capitalize() for part in name_parts]
    return ' '.join(capitalized_name_parts)

inventors = []
for patent in dataset:
    inventors.extend(patent["inventors"])

inventor_names = [to_sentence_case(inventor.get("inventor_name")) for inventor in inventors if "inventor_name" in inventor]

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["inventors_circle"]
    users_collection = db["users"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()

users = list(users_collection.find())

for user in users:
    recommendations = random.sample(
        [name for name in inventor_names if name != user["name"]],
        k=10
    )
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"recommendations": recommendations}}
    )

print("Recommendations successfully added to MongoDB!")