# Hello World Project

A simple, world-class "Hello World" application written in Python.

## Description

This project demonstrates the most fundamental concept in programming: displaying "Hello World" to the console. While simple, this project follows best practices including proper documentation and a clean, maintainable structure.

## Requirements

- Python 3.x
- Docker (optional, for containerized deployment)
- GitHub Personal Access Token (for GitHub credentials extraction)

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

### Extracting GitHub Credentials

To extract GitHub Actions secrets and variables and save them to creds.txt:

1. Set your GitHub token as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_github_token
   ```

2. Run the main script with the extract-creds flag:
   ```bash
   python main.py --extract-creds
   ```

This will create or update the creds.txt file with all GitHub Actions secrets and variables from the repository.

## Project Structure

- `main.py`: Contains the Python code that prints "Hello World" to the console
- `github_creds.py`: Script for extracting GitHub Actions secrets and variables
- `creds.txt`: File containing GitHub Actions secrets and variables
- `README.md`: This file, containing project documentation
- `Dockerfile`: Configuration for building a Docker image of the application
- `.dockerignore`: Specifies files to exclude from the Docker build context
- `test_main.py`: Unit tests for the main functionality
- `test_github_creds.py`: Unit tests for the GitHub credentials extraction functionality
- `test_docker.py`: Tests for Docker functionality

## Expected Output

When you run the program, you should see the following output:

```
Hello World
```

When you run with the `--extract-creds` flag, the program will additionally extract GitHub credentials and save them to creds.txt.
