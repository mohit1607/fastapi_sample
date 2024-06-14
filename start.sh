#!/bin/bash

cd "$(dirname "$0")"
source .env/bin/activate
uvicorn app:app --host=0.0.0.0 --port=8000 --workers=4