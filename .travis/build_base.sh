#!/usr/bin/env bash

docker build -t fastapi-app .

# docker exec fastapi-app -t ./bin/boot.sh