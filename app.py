from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from datetime import datetime, timezone
import gunicorn

app = Flask(__name__)
load_dotenv()

app.config["MONGO_URI"] = os.getenv("DATABASE_URL")
CORS(
    app,
    resources={r"/*": {"origins": "https://mapified-frontend.onrender.com"}},
    supports_credentials=True,
)
print("CORS registered for routes:", app.url_map)
mongo = PyMongo(app)
mongo.init_app(app)
pins_collection = mongo.db.pins


@app.before_request
def log_request():
    print("Incoming request:", request.method, request.path)
    print("Headers:", request.headers)


@app.route("/pins", methods=["GET", "OPTIONS"])
def get_pins():
    pins = []
    for pin in pins_collection.find({}, {"_id": 0}):
        if "location" in pin:
            pin["lat"] = pin["location"]["coordinates"][1]
            pin["lng"] = pin["location"]["coordinates"][0]
        if "created_at" in pin:
            pin["created_at"] = pin["created_at"].isoformat()
        pins.append(pin)

    return jsonify(pins)


@app.route("/pins", methods=["POST", "OPTIONS"])
def new_pin():
    data = request.json
    if (
        "lat" not in data
        or "lng" not in data
        or "spotify_url" not in data
        or not data["spotify_url"].strip()
    ):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    pin_doc = {
        "text": data.get("text", "").strip(),
        "spotify_url": data["spotify_url"].strip(),
        "location": {"type": "Point", "coordinates": [data["lng"], data["lat"]]},
        "created_at": datetime.now(timezone.utc),
    }
    pins_collection.insert_one(pin_doc)
    return jsonify({"status": "success"}), 201


gunicorn app:app --bind 0.0.0.0:$PORT
