import json
import random
from user_recommendations import InventorRecommender
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description="Insert users into MongoDB.")
parser.add_argument("--user", required=True, help="MongoDB username")
parser.add_argument("--password", required=True, help="MongoDB password")
args = parser.parse_args()

MONGO_URI = f"mongodb+srv://{args.user}:{args.password}@cluster0.8cy6qn7.mongodb.net/"

with open("../dataset/patents.json", "r") as file:
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
    client = MongoClient(MONGO_URI)
    db = client["inventors_circle"]
    users_collection = db["users"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()

users = list(users_collection.find())

recommender = InventorRecommender("../dataset/patents.json")
recommender.initialize()

for user in users:
    '''
    recommendations = random.sample(
        [name for name in inventor_names if name != user["name"]],
        k=10
    )
    '''
    recommendations = recommender.recommend_inventors(user["name"])
    #print(f"\nTop Inventor Recommendations for {inventor_name}: {recommendations}")
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"recommendations": recommendations}}
    )

print("Recommendations successfully added to MongoDB!")