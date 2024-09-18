#!/bin/bash
NOW=$(date +"%Y-%m-%d")
REPO=registry.ayuda.la/public
IMAGE=thermal-printer-api

docker build --no-cache -t ${REPO}/${IMAGE}:${NOW} -t ${REPO}/${IMAGE}:latest .
docker push ${REPO}/${IMAGE}:${NOW}
docker push ${REPO}/${IMAGE}:latest