import pymongo
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up logger to file
logging.basicConfig(
    filename="logs/app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: str

# Check for testing environment - If MONGO_URI is not set, we assume this is the test environment
if os.getenv("MONGO_URI"):
    # MongoDB for production
    import pymongo
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.get_database()
else:  
    # Mocking the MongoDB behavior
    from unittest.mock import MagicMock
    db = MagicMock()


## Health check, can be later used in K8S health checks
@app.route("/health", methods=["GET"])
def health_check():
    logger.warning("GET request to /health endpoint")
    return jsonify({"status": "200"})

## Getting all items from the DB - convertion of object_id to string is required
@app.route("/items", methods=["GET"])
def read_items():
    logger.warning("GET request to /items endpoint")
    try:
        items = list(db.items.find())
        for item in items:
            item['_id'] = str(item['_id'])
        if not items:
            logger.warning("No items found in the database.")
        return jsonify(items)
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return jsonify({"error": "Failed to fetch items"}), 500

## Pushing json file into the db by using unpacking item_data into keywords, for the Item validation
@app.route("/input", methods=["POST"])
def create_item():
    item_data = request.get_json()
    item = Item(**item_data)
    db.items.insert_one(item.dict()) 
    logger.warning(f"Item created: {item.dict()}")
    return jsonify({"message": "Item created successfully", "item": item.dict()}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
