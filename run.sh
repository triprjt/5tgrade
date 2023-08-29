#!/bin/bash

# Build the Docker image
docker build -t my-django-app .

# Run the Docker container
docker run -p 8000:8000 my-django-app