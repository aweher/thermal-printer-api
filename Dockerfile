# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Labels for the Docker image
LABEL maintainer="Ariel S. Weher <ariel@weher.net>"
LABEL version="1.0"
LABEL description="This is a Docker image for the Epson TM-m30ii API"
LABEL org.opencontainers.image.source="https://github.com/aweher/thermal-printer-api"
LABEL org.opencontainers.image.licenses="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_ENV=production

# Command to run the app using Gunicorn for better production performance
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
