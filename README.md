# Microservice Projectsss

## Overview
This project demonstrates a basic microservice architecture with a REST API, MongoDB integration, logging, and containerized deployment using Kubernetes. The image is built and pushed to DockerHub automatically through GitHub Actions.

---

## Features
- **REST API Endpoints**:
  - `GET /health`: Service health check.
  - `POST /input`: Add an item to the database.
  - `GET /items`: Retrieve all items.
- **Database**: MongoDB or another database of choice.

---

## Requirements
To run this project, ensure the following are installed:

- **Kubernetes**: Required for deployment.
- **Helm**: Used to manage Kubernetes resources.
---

## CI/CD Pipeline (GitHub Actions)
The pipeline is fully automated via **GitHub Actions**.The trigger is pushing to the main branch and it includes:
1. **Unit Tests**: Ensures code quality.
2. **Docker Build & Push**: Builds the image and pushes it to DockerHub.
3. **Kubernetes Rollout**: Rollouts the application to the Kubernetes cluster using Helm.

There is no need for manual intervention in the pipeline as everything is handled automatically through GitHub Actions.

---

## Deploy to Kubernetes
Deploy the application to Kubernetes using Helm:
```
helm install <release_name> k8s_microservice/
```


## Testing
Unit tests are executed as part of the GitHub Actions pipeline. However, if you'd like to run them locally, use:
```
pytest src/test.py
```
---
## Files Structure
```
├── Dockerfile
├── pyproject.toml
├── README.md
├── src
|    ├── gunicorn_conf.py
|    ├── main.py
|    └── test.py
└── k8s_microservice
     ├── Chart.yaml
     ├── values.yaml
     └── templates
         ├── deployment.yaml
         ├── ingress.yaml
         ├── pvc.yaml
         ├── pv.yaml
         └── service.yaml

```