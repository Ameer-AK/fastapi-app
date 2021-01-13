#!/usr/bin/env bash

docker build -t fastapi-app-test --build-arg EXTRA_REQUIREMENTS=test-requirements.txt .
