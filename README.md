# Hello World Project

A simple, world-class "Hello World" application written in Python.

## Description

This project demonstrates the most fundamental concept in programming: displaying "Hello World" to the console. While simple, this project follows best practices including proper documentation and a clean, maintainable structure.

## Requirements

- Python 3.x
- Docker (optional, for containerized deployment)

## How to Run

### Using Python directly

Execute the main.py file using Python:

```bash
python main.py
```

Or make the file executable and run it directly:

```bash
chmod +x main.py
./main.py
```

### Using Docker

Build the Docker image:

```bash
docker build -t hello-world .
```

Run the Docker container:

```bash
docker run --rm hello-world
```

## GitHub Actions Credentials

This project includes functionality to work with GitHub Actions secrets and variables:

- `creds.txt`: Contains GitHub Actions secrets and variables in key-value format
- `github_creds.py`: Script to extract GitHub Actions secrets and variables from the environment
- `read_credentials()` function in `main.py`: Utility to read and parse the credentials file

To extract GitHub Actions secrets and variables (when running in a GitHub Actions workflow):

```bash
python github_creds.py
```

## Project Structure

- `main.py`: Contains the Python code that prints "Hello World" to the console
- `README.md`: This file, containing project documentation
- `Dockerfile`: Configuration for building a Docker image of the application
- `.dockerignore`: Specifies files to exclude from the Docker build context
- `creds.txt`: Contains GitHub Actions secrets and variables
- `github_creds.py`: Script to extract GitHub Actions secrets and variables
- `test_main.py`, `test_docker.py`, `test_credentials.py`: Test files for the application

## Expected Output

When you run the program, you should see the following output:

```
Hello World
```
