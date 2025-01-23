import pymongo
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up template for logging to file
logging.basicConfig(
    filename="logs/app.log",  # Log file name
    level=logging.WARNING,  # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
)
logger = logging.getLogger(__name__)  # Create logger for this file

# Define Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: str

# Check for testing environment - If MONGO_URI is not set, we assume this is the test environment
if os.getenv("MONGO_URI"):
    # MongoDB for production
    import pymongo
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.get_database()  # This will be the real DB
else:  
    # Mocking the MongoDB behavior
    from unittest.mock import MagicMock
    db = MagicMock()  # Create a mock object


## Health check, can be later used in K8S health checks
@app.route("/health", methods=["GET"])
def health_check():
    logger.warning("GET request to /health endpoint")
    return jsonify({"status": "200"})

## Getting all items from the DB
@app.route("/items", methods=["GET"])
def read_items():
    logger.warning("GET request to /items endpoint")
    try:
        items = list(db.items.find())  # Ensure the cursor is fully consumed into a list
        for item in items:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON compatibility - needed in order to pull the data
        if not items:
            logger.warning("No items found in the database.")  # Log if no items are found
        return jsonify(items)
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return jsonify({"error": "Failed to fetch items"}), 500

## Pushing json file into the db
@app.route("/input", methods=["POST"])
def create_item():
    item_data = request.get_json()
    item = Item(**item_data) ## Unpacking item_data into keywords, for the Item validation
    db.items.insert_one(item.dict()) 
    logger.warning(f"Item created: {item.dict()}")
    return jsonify({"message": "Item created successfully", "item": item.dict()}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
