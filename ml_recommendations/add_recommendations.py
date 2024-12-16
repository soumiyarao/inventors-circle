import json
from contest_based_recommender import InventorRecommenderCB
from collaborative_recommender import InventorRecommenderCF
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description="Insert users into MongoDB.")
parser.add_argument("--user", required=True, help="MongoDB username")
parser.add_argument("--password", required=True, help="MongoDB password")
args = parser.parse_args()

MONGO_URI = f"mongodb+srv://{args.user}:{args.password}@cluster0.8cy6qn7.mongodb.net/"

with open("../dataset/patents.json", "r") as file:
    dataset = json.load(file)

try:
    client = MongoClient(MONGO_URI)
    db = client["inventors_circle"]
    users_collection = db["users"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()


users = list(users_collection.find())

recommender_cb = InventorRecommenderCB("../dataset/patents.json")
recommender_cb.initialize()

recommender_cf = InventorRecommenderCF(users_collection)
recommender_cf.initialize()

for user in users:
    recommendations_cb = recommender_cb.recommend_inventors(user["name"], top_n=10)
    recommendations_cf = recommender_cf.recommend_inventors(user["name"], top_n=10)

    top_cb = recommendations_cb[:6]
    top_cf = recommendations_cf[:4]

    final_recommendations = set()

    for name, _ in top_cb:
        final_recommendations.add(name)

    for name, _ in top_cf:
        final_recommendations.add(name)

    #print(final_recommendations)

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"recommendations": list(final_recommendations)}}
    )

print("Recommendations successfully added to MongoDB!")