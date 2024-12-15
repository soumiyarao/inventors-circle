import json
from pymongo import MongoClient
import argparse

def to_sentence_case(name):
    name_parts = name.split()
    capitalized_name_parts = [part.capitalize() for part in name_parts]
    return ' '.join(capitalized_name_parts)

parser = argparse.ArgumentParser(description="Insert users into MongoDB.")
parser.add_argument("--user", required=True, help="MongoDB username")
parser.add_argument("--password", required=True, help="MongoDB password")
args = parser.parse_args()

MONGO_URI = f"mongodb+srv://{args.user}:{args.password}@cluster0.8cy6qn7.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["inventors_circle"]
users_collection = db["users"]

with open("../dataset/patents.json", "r") as file:
    patents_data = json.load(file)

users = list(users_collection.find())

for user in users:
    user_name = user["name"]

    matching_patents = [
        patent for patent in patents_data 
        if any(
            to_sentence_case(inventor.get("inventor_name")) == user_name 
                for inventor in patent.get("inventors", [])
                if "inventor_name" in inventor
            )
    ]
    
    branches = set()
    organizations = set()
    
    for patent in matching_patents:
        if "branch" in patent:
            branches.add(patent["branch"])
        if "applicants" in patent:
            for applicant in patent["applicants"]:
                if "organization" in applicant:
                    organizations.add(to_sentence_case(applicant["organization"]))
    
    branches_list = list(branches)
    organizations_list = list(organizations)
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "about": branches_list,
            "organizations": organizations_list
        }}
    )

print("User records updated successfully!")