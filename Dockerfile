# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables
ENV MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
ENV MINIO_SECRET_KEY=${MINIO_SECRET_KEY}

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY wait-for-it.sh /app/wait-for-it.sh

# Ensure the entrypoint script is executable
RUN chmod +x /app/wait-for-it.sh

# Copy the rest of the application code into the container
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Use the entrypoint script to start the container
ENTRYPOINT ["./wait-for-it.sh"]
