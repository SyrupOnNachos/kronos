#!/bin/bash
ENV=${ENV:-local}
if [ "$ENV" == "local" ]
then
    pipenv run uvicorn main:app --reload --port 80 --host 0.0.0.0
else
    pipenv install
    pipenv run uvicorn main:app --port $PORT --host 0.0.0.0
fi
