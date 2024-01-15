#!/bin/bash
ENV=${ENV:-local}
if [ "$ENV" == "local" ]
then
    # Start Uvicorn with debugpy on port 5678
    pipenv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn main:app --reload --port 80 --host 0.0.0.0
else
    pipenv install
    pipenv run uvicorn main:app --port $PORT --host 0.0.0.0
fi
