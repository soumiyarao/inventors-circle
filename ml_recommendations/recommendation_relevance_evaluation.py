from pymongo import MongoClient
from bson import ObjectId
import argparse

# Command-line argument parser
parser = argparse.ArgumentParser(description="Evaluate recommendation model.")
parser.add_argument("--user", required=True, help="MongoDB username")
parser.add_argument("--password", required=True, help="MongoDB password")
args = parser.parse_args()

# MongoDB connection
MONGO_URI = f"mongodb+srv://{args.user}:{args.password}@cluster0.8cy6qn7.mongodb.net/"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["inventors_circle"]
users_collection = db["users"]

# Fetch all users
all_users = users_collection.find()

# Metrics variables
total_relevance_scores = 0
total_users = 0
users_with_relevant_recommendations = 0
precision_at_k_sum = 0
recall_at_k_sum = 0
k = 10  # Define top K for precision and recall

print("Starting Evaluation of Model")

# Process each user
for current_user in all_users:
    user_id = current_user["_id"]
    recommendations = current_user.get("recommendations", [])

    # Total recommendations for the user
    total_recommendations = len(recommendations)
    if total_recommendations == 0:
        continue  # Skip users with no recommendations

    # Fetch followers, second-degree connections, and content-based matches
    followers = current_user.get("followers", [])
    following = current_user.get("following", [])
    branch = current_user.get("branch", None)
    organization = current_user.get("organization", None)

    follower_names = [
        f["name"] for f in users_collection.find({"_id": {"$in": followers}}, {"name": 1})
    ]
    second_degree_ids = users_collection.aggregate([
        {"$match": {"_id": {"$in": following}}},
        {"$project": {"following": 1}},
        {"$unwind": "$following"},
        {"$group": {"_id": None, "second_degree_ids": {"$addToSet": "$following"}}}
    ])
    second_degree_ids = next(second_degree_ids, {}).get("second_degree_ids", [])
    second_degree_ids = list(set(second_degree_ids) - set(following) - {user_id})
    second_degree_names = [
        f["name"] for f in users_collection.find({"_id": {"$in": second_degree_ids}}, {"name": 1})
    ]
    content_based_names = [
        f["name"] for f in users_collection.find(
            {"branch": branch, "organization": organization, "_id": {"$ne": user_id}}, {"name": 1}
        )
    ]

    # Identify relevant recommendations
    relevant_recommendations = set(follower_names + second_degree_names + content_based_names)
    relevant_count = len(relevant_recommendations & set(recommendations))

    # Update metrics
    total_relevance_scores += relevant_count / total_recommendations  # Relevance Score
    total_users += 1
    if relevant_count > 0:
        users_with_relevant_recommendations += 1

    # Calculate Precision@K
    top_k_recommendations = recommendations[:k]
    relevant_in_top_k = len(set(top_k_recommendations) & relevant_recommendations)
    precision_at_k = relevant_in_top_k / k
    recall_at_k = relevant_in_top_k / len(relevant_recommendations) if len(relevant_recommendations) > 0 else 0  # Avoid division by zero

    precision_at_k_sum += precision_at_k
    recall_at_k_sum += recall_at_k

# Compute final metrics
mean_relevance_score = total_relevance_scores / total_users if total_users > 0 else 0
coverage = users_with_relevant_recommendations / total_users if total_users > 0 else 0
average_precision_at_k = precision_at_k_sum / total_users if total_users > 0 else 0
average_recall_at_k = recall_at_k_sum / total_users if total_users > 0 else 0

print("Total Users:" , total_users)
print("Evaluation Metrics For Hybrid Recommendations Model:")
print(f"Hit Rate: {coverage:.2%}")
print(f"Average Precision@{k}: {average_precision_at_k:.2%}")

