# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /usr/src/app
COPY ../Pipfile ../Pipfile.lock ./

# Install dependencies in a virtual environment
RUN pipenv install --deploy --ignore-pipfile

# Copy your application code
COPY ../api ./api

# Expose the port the app runs on
EXPOSE 80

# Run the application using Pipenv in a virtual environment
CMD ["pipenv", "run", "uvicorn", "api.nfc_reader:app", "--host", "0.0.0.0", "--port", "80"]
