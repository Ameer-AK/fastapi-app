#!/usr/bin/env bash

docker build -t fastapi-app --build-arg EXTRA_REQUIREMENTS=requirements.txt .
