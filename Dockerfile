FROM python:3.13.5-slim

# Install FFmpeg, git, and other dependencies
RUN apt-get update && apt-get install -y ffmpeg git

# Set the working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install any necessary Python packages (e.g., pip install -r requirements.txt)
RUN pip install -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "main.py"]