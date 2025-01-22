# Microservice with FastAPI and MongoDB

This is a basic microservice built with FastAPI and MongoDB.

## Features
- FastAPI for building the API
- Gunicorn for production-ready serving
- MongoDB for data storage
- Python-dotenv for environment variables management

## Setup
1. Clone the repository.
2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. Start the application using Docker:
    ```bash
    docker build -t microservice .
    docker run -p 8000:8000 microservice
    ```
4. Access the API at `http://localhost:8000`.


