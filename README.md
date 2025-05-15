# Hello World Project

A simple, world-class "Hello World" application written in Python.

## Description

This project demonstrates the most fundamental concept in programming: displaying "Hello World" to the console. While simple, this project follows best practices including proper documentation and a clean, maintainable structure.

## Requirements

- Python 3.x
- Docker (optional, for containerized deployment)
- GitHub Personal Access Token (for credential extraction functionality)

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

### Extracting GitHub Actions Secrets and Variables

This project includes functionality to extract GitHub Actions secrets and variables from a repository and write them to a file.

Prerequisites:
- A GitHub Personal Access Token with `repo` scope
- Python requests library (`pip install requests`)

To extract credentials:

```bash
# Set your GitHub token as an environment variable
export GITHUB_TOKEN=your_github_token

# Run the extraction script
python extract_creds.py
```

This will create a `creds.txt` file in the project root containing all GitHub Actions secrets and variables.

Advanced usage:

```bash
# Specify a custom output file
python extract_creds.py --output /path/to/output.txt

# Provide the token directly
python extract_creds.py --token your_github_token

# Specify a specific repository
python extract_creds.py --repo owner/repo
```

## Project Structure

- `main.py`: Contains the Python code that prints "Hello World" to the console
- `README.md`: This file, containing project documentation
- `Dockerfile`: Configuration for building a Docker image of the application
- `.dockerignore`: Specifies files to exclude from the Docker build context
- `github_creds.py`: Module for accessing GitHub Actions secrets and variables
- `extract_creds.py`: Command-line interface for extracting credentials
- `creds.txt`: Generated file containing GitHub Actions secrets and variables

## Expected Output

When you run the main program, you should see the following output:

```
Hello World
```

When you run the credential extraction script, you should see output similar to:

```
Repository: owner/repo
Retrieving GitHub Actions secrets...
Found X secrets
Retrieving GitHub Actions variables...
Found Y variables
Successfully wrote credentials to creds.txt
```
