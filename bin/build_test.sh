#!/usr/bin/env bash

docker build -t fastapi-app-test --build-arg EXTRA_REQUIREMENTS=test-requirements.txt .

docker exec fastapi-app-test -t ./bin/test.sh