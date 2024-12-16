import random
from pymongo import MongoClient
import argparse

def update_following():
    all_users = list(users_collection.find())
    for user in all_users:
        recommendations = user.get("recommendations", [])
        
        num_recommended = random.randint(0, 3)
        recommended_following = random.sample(recommendations, num_recommended) if recommendations else []
        recommended_following_ids = [u["_id"] for u in all_users if u["name"] in recommended_following]
        
        non_recommended_ids = [u["_id"] for u in all_users if u["_id"] != user["_id"] and u["name"] not in recommendations]
        num_non_recommended = random.randint(1, 5)
        non_recommended_following_ids = random.sample(non_recommended_ids, num_non_recommended)
        
        combined_following = recommended_following_ids + non_recommended_following_ids
        updated_following = [user_id for user_id in combined_following if user_id != user["_id"]]

        users_collection.update_one({"_id": user["_id"]}, {"$set": {"following": updated_following}})
    
    print("Following list updated for all users successfully!")

def update_followers():
    all_users = list(users_collection.find())
    for user in all_users:
        followers = []
        for other_user in all_users:
            if (user["_id"] != other_user["_id"]) and (user["_id"] in other_user.get("following", [])):
                followers.append(other_user["_id"])
        
        users_collection.update_one({"_id": user["_id"]}, {"$set": {"followers": followers}})
    
    print("Following list updated for all users successfully!")

parser = argparse.ArgumentParser(description="Insert users into MongoDB.")
parser.add_argument("--user", required=True, help="MongoDB username")
parser.add_argument("--password", required=True, help="MongoDB password")
args = parser.parse_args()

MONGO_URI = f"mongodb+srv://{args.user}:{args.password}@cluster0.8cy6qn7.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["inventors_circle"]
users_collection = db["users"]

update_following()
update_followers()