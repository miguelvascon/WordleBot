# Base image with Python
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium and ChromiumDriver
RUN apt-get update && \
    apt-get install -y wget unzip chromium chromium-driver

# Copy all the code into the container
COPY . .

# Set environment variable to specify ChromiumDriver path
ENV PATH="/usr/lib/chromium:$PATH"

# Run the bot script when the container starts
CMD ["python", "src/main.py"]
