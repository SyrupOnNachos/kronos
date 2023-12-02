# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /usr/src/app
COPY ./Pipfile ./Pipfile.lock ./

# Install dependencies in a virtual environment
RUN pipenv install --deploy --ignore-pipfile

# Copy your main FastAPI application entrypoint
COPY ./main.py ./main.py

# Copy your application code
COPY ./api ./api

# Copy your application code
COPY ./models ./models

# Expose the port the app runs on
EXPOSE 8080

# Run the application using Pipenv in a virtual environment
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
