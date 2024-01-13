# Use an official Python runtime as a base image
FROM python:3.11
# Set the working directory in the container
WORKDIR /usr/src/app
# Install pipenv
RUN pip install pipenv
RUN pip install uvicorn

# Copy the Pipfile and Pipfile.lock into the container at /usr/src/app
COPY ./Pipfile ./Pipfile.lock ./requirements.txt ./

# Install dependencies in a virtual environment
RUN pipenv install --deploy --ignore-pipfile

COPY ./main.py ./main.py
COPY ./api ./api
COPY ./models ./models
COPY entrypoint.sh .


RUN chmod a+x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
