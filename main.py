from flask import Flask, request, jsonify
import pymongo
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()

# Define Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: str

# Set up logging to file
logging.basicConfig(
    filename="/app/logs/app.log",  # Log file name
    level=logging.WARNING,  # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
)
logger = logging.getLogger(__name__)  # Create logger for this file

@app.route("/health", methods=["GET"])
def read_root():
    logger.warning("GET request to root endpoint")  # Log info message
    return jsonify({"status": "200"})

@app.route("/items", methods=["GET"])
def read_items():
    logger.warning("GET request to /items endpoint")  # Log info message
    items = list(db.items.find())  # Get all items from MongoDB
    for item in items:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON compatibility
    return jsonify(items)

@app.route("/input", methods=["POST"])
def create_item():
    item_data = request.get_json()
    item = Item(**item_data)  # Validate incoming data using Pydantic
    # Insert a new item into the database
    logger.warning(f"Item created: {item.dict()}")  # Log info message
    db.items.insert_one(item.dict())
    return jsonify({"message": "Item created successfully", "item": item.dict()}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)