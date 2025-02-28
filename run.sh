#!/bin/bash
docker build -t mistral-gguf-api . && docker run --rm -p 8000:8000 mistral-gguf-api
