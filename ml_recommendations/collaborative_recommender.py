from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np

class InventorRecommenderCF:
    def __init__(self, users_collection):
        self.users = list(users_collection.find({}))
        self.user_id_map = {}
        self.knn = NearestNeighbors(metric="cosine", algorithm="brute")
        self.mutual_connections_matrix = None

    def initialize(self):
        self.user_id_map = {str(user["_id"]): i for i, user in enumerate(self.users)}

        num_users = len(self.users)
        rows, cols, data = [], [], []

        for user in self.users:
            user_idx = self.user_id_map[str(user["_id"])]
            for conn_type in ("followers", "following"):
                for conn_id in map(str, user.get(conn_type, [])):
                    if conn_id in self.user_id_map:
                        conn_idx = self.user_id_map[conn_id]
                        rows.append(user_idx)
                        cols.append(conn_idx)
                        data.append(1)

        direct_connections_matrix = csr_matrix((data, (rows, cols)), shape=(num_users, num_users))
        indirect_connections_matrix = direct_connections_matrix.dot(direct_connections_matrix)
        indirect_connections_matrix.setdiag(0)

        self.mutual_connections_matrix = direct_connections_matrix + indirect_connections_matrix

        self.knn.fit(self.mutual_connections_matrix)

    def recommend_inventors(self, inventor_name, top_n=10):
        target_user = next((u for u in self.users if u["name"] == inventor_name), None)
        if not target_user:
            print(f"User '{inventor_name}' not found.")
            return

        target_idx = self.user_id_map[str(target_user["_id"])]
        distances, indices = self.knn.kneighbors(self.mutual_connections_matrix[target_idx], n_neighbors=top_n + 1)
        
        recommendations = [
            (self.users[idx]["name"], dist)
            for idx, dist in zip(indices.flatten(), distances.flatten())
            if idx != target_idx
        ]

        #print(recommendations)
        return recommendations
