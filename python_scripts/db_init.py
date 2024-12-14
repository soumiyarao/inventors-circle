import json
import random
import hashlib
import hmac
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
import re

with open("ds_patent_dataset.json", "r") as file:
    dataset = json.load(file)

unique_inventors_dict = {}
for patent in dataset:
    for inventor in patent["inventors"]:
        if "inventor_name" in inventor:
            unique_inventors_dict[inventor["inventor_name"]] = inventor

inventors = list(unique_inventors_dict.values())

#selected_inventors = random.sample(inventors, 20)

def to_sentence_case(name):
    name_parts = name.split()
    capitalized_name_parts = [part.capitalize() for part in name_parts]
    return ' '.join(capitalized_name_parts)

def generate_user_data(inventor):
    name_parts = inventor["inventor_name"].split()
    first_name = name_parts[0].lower()
    last_name = ''
    if len(name_parts) > 1:
        last_name += inventor["inventor_name"].split()[1].lower()
    
    password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))
    salt = str(random.randint(100000, 999999))
    hashed_password = hmac.new(salt.encode(), password.encode(), hashlib.sha1).hexdigest()
    
    return {
        "_id": ObjectId(),
        "following": [],
        "followers": [],
        "name": to_sentence_case(inventor["inventor_name"]),
        "email": f"{first_name}_{last_name}@gmail.com",
        "salt": salt,
        "password": password,
        "hashed_password": hashed_password,
        "created": datetime.now().isoformat(),
        "__v": 0
    }

users = [generate_user_data(inventor) for inventor in inventors if "inventor_name" in inventor]
#print(users)

users_without_password = [
    {k: v for k, v in user.items() if k != "password"}
    for user in users
]

def serialize_object_ids(users):
    for user in users:
        if '_id' in user:
            user['_id'] = str(user['_id'])
    return users

users_serializable = serialize_object_ids(users)

with open("users.json", "w") as outfile:
    json.dump(users_serializable, outfile, indent=4)

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["inventors_circle"]
    users_collection = db["users"]
    
    users_collection.insert_many(users_without_password)
    print("Users successfully inserted into MongoDB!")
except Exception as e:
    print(f"An error occurred while inserting into MongoDB: {e}")