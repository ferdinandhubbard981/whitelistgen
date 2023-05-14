#!/bin/bash

echo "Building whitelistgen..."
cd sumlecpy
docker build -t whitelistgen .
cd ..



docker image prune -f

echo "Docker image built successfully!"
