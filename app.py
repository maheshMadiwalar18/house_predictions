from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # allow frontend requests

# load model
try:
    with open("house_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model file not found"}), 500
        
    try:
        data = request.get_json()

        # Ensure EXACT feature order: [area, bedrooms, bathrooms, age]
        # and ensure they are numeric
        features = np.array([
            float(data["area"]),
            float(data["bedrooms"]),
            float(data["bathrooms"]),
            float(data["age"])
        ]).reshape(1, -1)

        prediction = model.predict(features)

        # Return as "price" as per requirement
        return jsonify({
            "price": float(prediction[0])
        })

    except Exception as e:
        return jsonify({"error": "Invalid input data"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=False)
