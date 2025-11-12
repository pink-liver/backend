# backend

A simple Flask API for backend.

## Features

- Ranking game scores

## Docker

### Build Docker Image

```bash
docker build -t backend .
```

### Run Docker Container

1. Using Environment Variables

```bash
docker run \
  -p 8080:8080 \
  -v $(pwd)/backend/files:/app/files \
  -e AUTO_SAVE_INTERVAL=30 \
  backend
```

2. Using Volume Mount for Configuration Files

```bash
docker run \
  -p 8080:8080 \
  -v $(pwd)/backend/files:/app/files \
  -v $(pwd)/backend/config/custom_settings.py:/app/config/settings.py \
  backend
```
