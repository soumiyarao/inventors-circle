from flask import Flask, request, jsonify
from contest_based_recommender import InventorRecommenderCB

app = Flask(__name__)
recommender = None

@app.route('/recommendations', methods=['POST'])
def recommend():
    data = request.get_json()
    name = data.get('inventor_name')
    if not name:
        return jsonify({"error": "Name is required"}), 400

    recommendations = recommender.recommend_inventors(name)    
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    recommender = InventorRecommenderCB("../dataset/patents.json")
    recommender.initialize()

    app.run(port=5000)