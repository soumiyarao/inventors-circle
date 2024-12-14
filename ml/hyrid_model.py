from pymongo import MongoClient
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np
import logging
from time import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Connect to MongoDB cloud database
mongo_uri = "mongodb+srv://aparnabharathi:aparnabharathi@inventorrecommendations.mbvnl.mongodb.net/"
client = MongoClient(mongo_uri)
db = client['inv']  # Replace with your database name
users_collection = db['inventor']

# Fetch user data from MongoDB
logging.info("Fetching user data from MongoDB...")
start_time = time()
users = list(users_collection.find({}))
num_users = len(users)
logging.info(f"Fetched {num_users} records from the database in {time() - start_time:.2f} seconds.")

# Simulated content-based vectors (replace with real content features if available)
logging.info("Generating random content vectors for content-based similarity...")
content_vectors = np.random.rand(num_users, 5).astype('float32')  # Use float32 for reduced memory

# Collaborative similarity: Sparse matrix representation
logging.info("Building collaborative similarity sparse matrix...")
row, col, data = [], [], []

for i, user in enumerate(users):
    user_followers = {f.get('email') for f in user.get('followers', []) if isinstance(f, dict)}
    user_following = {f.get('email') for f in user.get('following', []) if isinstance(f, dict)}

    for j, other_user in enumerate(users):
        if i != j:
            other_followers = {f.get('email') for f in other_user.get('followers', []) if isinstance(f, dict)}
            other_following = {f.get('email') for f in other_user.get('following', []) if isinstance(f, dict)}

            # Compute shared followers and following
            shared_followers = user_followers.intersection(other_followers)
            shared_following = user_following.intersection(other_following)

            # Add similarity score to sparse matrix if non-zero
            similarity = len(shared_followers) + len(shared_following)
            if similarity > 0:
                row.append(i)
                col.append(j)
                data.append(similarity)

    if i % 1000 == 0:  # Log progress every 1000 users
        logging.info(f"Processed {i}/{num_users} users for collaborative similarity.")

# Create sparse collaborative matrix
collab_matrix = csr_matrix((data, (row, col)), shape=(num_users, num_users), dtype='float32')

# Normalize collaborative similarity
logging.info("Normalizing collaborative similarity sparse matrix...")
if collab_matrix.max() > 0:
    collab_matrix = collab_matrix / collab_matrix.max()

# Content-based similarity using NearestNeighbors
logging.info("Calculating content-based similarity using Nearest Neighbors...")
n_neighbors = 10  # Number of recommendations per user
nbrs = NearestNeighbors(n_neighbors=n_neighbors + 1, metric='cosine', algorithm='brute')
nbrs.fit(content_vectors)
distances, indices = nbrs.kneighbors(content_vectors)

# Generate recommendations in batches
logging.info("Generating and updating hybrid recommendations in batches...")
alpha, beta = 0.5, 0.5  # Weights for hybridization

for user_index, user in enumerate(users):
    # Hybrid similarity for the current user
    hybrid_scores = collab_matrix[user_index].toarray().flatten() * alpha

    for j, neighbor_idx in enumerate(indices[user_index][1:]):  # Exclude self
        hybrid_scores[neighbor_idx] += beta * (1 - distances[user_index][j + 1])  # Invert distance for similarity

    # Get top N recommendations
    top_indices = hybrid_scores.argsort()[::-1][:n_neighbors]
    recommendations = [users[i]['name'] for i in top_indices if i < len(users)]

    # Update recommendations in MongoDB
    users_collection.update_one(
        {'_id': user['_id']},  # Match user by MongoDB's unique ID
        {'$set': {'recommendations': recommendations}}  # Update recommendations field
    )

    if user_index % 1000 == 0:  # Log progress every 1000 users
        logging.info(f"Updated recommendations for {user_index}/{num_users} users.")

logging.info("Hybrid recommendations have been successfully updated in the MongoDB database.")