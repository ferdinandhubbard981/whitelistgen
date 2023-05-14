#!/bin/sh
docker run -v "$PWD":/app/content --rm whitelistgen python whitelistgenerator.py -dir /app/content -input transcript.txt -output whitelistpart.txt