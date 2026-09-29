# Healthping

FastAPI backend application with automated tests, code quality checks, Docker support, and Kubernetes deployment.

## Tech Stack

* Python
* FastAPI
* Pytest
* Docker
* Kubernetes
* GitHub Actions

## Project Structure

```
.
├── .github/workflows/   # CI workflows
├── Codereview/          # Code review tools
├── Requirements/        # Project requirements
├── k8s/                 # Kubernetes manifests
├── tests/               # Tests
├── Dockerfile           # Docker configuration
└── pytest.ini           # Pytest configuration
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Tests

Run tests with:

```bash
pytest
```

## Docker

Build the image:

```bash
docker build -t healthping .
```

Run the container:

```bash
docker run -p 8000:8000 healthping
```

## Kubernetes

Kubernetes manifests are located in the `k8s/` directory.

```bash
kubectl apply -f k8s/
```

Check running pods:

```bash
kubectl get pods
```

## CI

GitHub Actions workflows are located in `.github/workflows/` and are used for automated testing and code quality checks.
