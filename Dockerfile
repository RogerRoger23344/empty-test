# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a non-root user and switch to it for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run main.py when the container launches
CMD ["python", "main.py"]