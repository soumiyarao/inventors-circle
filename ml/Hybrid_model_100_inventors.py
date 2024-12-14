import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np
import json

# Load JSON data
with open('C:/SJSU/Sem-2/DATA-236-Distributed Systems/Project/Work/patents_2.json') as f:
    data = json.load(f)

# Convert JSON data into a Pandas DataFrame
df = pd.json_normalize(data)

# Ensure the 'keywords' column exists
if 'keywords' in df.columns:
    # Combine normalized keywords into one string per row
    df['keywords_combined'] = df['keywords'].apply(
        lambda x: ' '.join([item['normalized_keyword'] for item in x]) if isinstance(x, list) else ''
    )
else:
    raise KeyError("The 'keywords' field is missing from the dataset.")

# Simulate a random user-patent interaction matrix
num_patents = df.shape[0]
num_users = 100  # Assume there are 100 users
interaction_matrix = csr_matrix(np.random.randint(0, 2, size=(num_users, num_patents)))

# Vectorize the combined keywords using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['keywords_combined'])

# Compute user-content matrix (user-patent interaction * patent content features)
user_content_matrix = interaction_matrix.dot(tfidf_matrix)  # This results in a (num_users, num_keywords) matrix

# Compute Content-based Similarity Between Users
content_sim_matrix = cosine_similarity(user_content_matrix)  # Now comparing users based on content (keywords)
content_sim_matrix_sparse = csr_matrix(content_sim_matrix)

# Compute Collaborative Filtering Similarity Between Users
collaborative_sim_matrix = cosine_similarity(interaction_matrix, interaction_matrix)
collaborative_sim_matrix_sparse = csr_matrix(collaborative_sim_matrix)

# Hybrid Recommendation: Combine Content and Collaborative Similarity
def hybrid_similarity(content_sim_matrix, collaborative_sim_matrix, alpha=0.5):
    return alpha * content_sim_matrix + (1 - alpha) * collaborative_sim_matrix

# Combine Content and Collaborative Similarity Matrices
final_sim_matrix = hybrid_similarity(content_sim_matrix_sparse, collaborative_sim_matrix_sparse)

# Function to generate recommendations for a single user
def generate_recommendations_with_user_name(sim_matrix, user_index, top_n=5):
    similarities = sim_matrix[user_index].toarray().flatten()
    similar_indices = similarities.argsort()[::-1][1:top_n + 1]
    inventor_names = df['inventors'].iloc[similar_indices].apply(lambda x: x[0]['inventor_name']).values
    return inventor_names.tolist()

# Generate recommendations for all users
all_recommendations = {}
for user_index in range(num_users):
    recommendations = generate_recommendations_with_user_name(final_sim_matrix, user_index, top_n=5)
    all_recommendations[f'user_{user_index}'] = recommendations

# Save recommendations to a JSON file
output_file = 'user_recommendations.json'
with open(output_file, 'w') as f:
    json.dump(all_recommendations, f, indent=4)

print(f"Recommendations for all users have been saved to {output_file}.")