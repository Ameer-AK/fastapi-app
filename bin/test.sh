#!/usr/bin/env bash

cd test

pytest -s --color=yes -v -rA --cov-report=term-missing --cov-fail-under=100 --cov=../src/controllers --cov=../src/models --cov=main
