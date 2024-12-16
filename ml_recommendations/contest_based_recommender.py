import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class InventorRecommenderCB:
    def __init__(self, patents_file):
        self.patents_file = patents_file
        self.dataset = None
        self.inventor_df = None
        self.similarity_matrix = None
    
    def initialize(self):
        with open(self.patents_file, "r") as file:
            self.dataset = json.load(file)

        self.inventor_df = self._preprocess_patents(self.dataset)
        self.similarity_matrix = self._compute_similarity(self.inventor_df)

    @staticmethod
    def _to_sentence_case(name):
        name_parts = name.split()
        capitalized_name_parts = [part.capitalize() for part in name_parts]
        return ' '.join(capitalized_name_parts)

    def _preprocess_patents(self, data):
        rows = []
        for patent in data:
            inventors = patent.get("inventors", [])
            keywords = " ".join([k["normalized_keyword"] for k in patent.get("keywords", [])])
            branch = patent.get("branch", "")
            code = patent.get("code", "")
            
            applicants = " ".join([applicant["organization"] for applicant in patent.get("applicants", [])])
            
            for inventor in inventors:
                inventor_name = inventor.get("inventor_name", "")
                state = inventor.get("state", "")
                combined_features = f"{keywords} {branch} {applicants} {state}"
                
                rows.append({
                    "inventor_name": self._to_sentence_case(inventor_name),
                    "combined_features": combined_features
                })

        return pd.DataFrame(rows)

    def _compute_similarity(self, df):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['combined_features'])
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return similarity_matrix

    def recommend_inventors(self, inventor_name, top_n=10):
        if inventor_name not in self.inventor_df['inventor_name'].values:
            print(f"Inventor {inventor_name} not found in dataset.")
            return []
        
        idx = self.inventor_df.index[self.inventor_df['inventor_name'] == inventor_name][0]
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_inventors = [
            (self.inventor_df.iloc[i]["inventor_name"], score)
            for i, score in similarity_scores[1:top_n+1]
        ]
        #print(top_inventors)
        return top_inventors
