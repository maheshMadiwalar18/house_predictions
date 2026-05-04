from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
import os

# Configure Flask to serve static files from the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# load model
try:
    with open("house_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model file not found"}), 500
        
    try:
        data = request.get_json()

        # Ensure EXACT feature order: [area, bedrooms, bathrooms, age]
        features = np.array([
            float(data["area"]),
            float(data["bedrooms"]),
            float(data["bathrooms"]),
            float(data["age"])
        ]).reshape(1, -1)

        prediction = model.predict(features)

        return jsonify({
            "price": float(prediction[0])
        })

    except Exception as e:
        return jsonify({"error": "Invalid input data"}), 400

if __name__ == "__main__":
    # Use environment port for deployment, default to 5000 for local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
