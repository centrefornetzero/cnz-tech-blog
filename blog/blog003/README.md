# Code Snippets for Blog003

### 1️⃣ `fastapidemo.py`
- Fast API demo app
- Imports Model from model.py

### 2️⃣ `Dockerfile`
- Dockerfile defining docker image
- Run this to build the docker image: `docker build -t blog003 .` -> this builds docker image with the image name = `blog003`
- Run this to launch the docker container: `docker run -p 8080:8080 blog003` -> this runs a container with image `blog003`, mapping port 8080 to 8080
- Access the FastAPI via this url: `http://localhost:8080/` when container is up and running

### 3️⃣ /github_actions/*
- `deploy_api_gateway.yaml`: Github workflow to deploy api gateway using `gcloud` commands
- `deploy_cloud_run.yaml`: Github workflow to deploy docker images to Google Cloud Run
- `docker_push.yaml`: Github workflow to build docker image and push to Google Artifact Registry
