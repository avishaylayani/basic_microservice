echo "Installing dependencies using Poetry..."
poetry install

# Build the Docker image
echo "Building Docker image..."
docker build -t microservice .

# Run the Docker container
echo "Running the Docker container..."
docker run -d -p 8000:8000 microservice

# Optionally, check the status of the container
echo "Container status:"
docker ps