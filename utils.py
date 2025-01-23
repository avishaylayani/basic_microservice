from pydantic import BaseModel
import logging
import json



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

## Add file operations for testing (When testing the api file without any container running)
def save_to_file(item, filename="test_items.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(item)
    with open(filename, "w") as f:
        json.dump(data, f)

def load_from_file(filename="test_items.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []