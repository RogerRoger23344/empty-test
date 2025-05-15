# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
RUN pip install --no-cache-dir requests

# Copy the current directory contents into the container at /app
COPY . /app

# Create a non-root user and switch to it for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set the entrypoint to allow different commands
ENTRYPOINT ["python"]

# Default command is to run main.py
CMD ["main.py"]