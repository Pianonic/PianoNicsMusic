# Use Python 3.13-5-slim as the base image
FROM python:3.13-5-slim

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install any necessary Python packages (e.g., pip install -r requirements.txt)
RUN pip install -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "main.py"]