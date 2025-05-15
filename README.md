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

## Project Structure

- `main.py`: Contains the Python code that prints "Hello World" to the console
- `README.md`: This file, containing project documentation
- `Dockerfile`: Configuration for building a Docker image of the application
- `.dockerignore`: Specifies files to exclude from the Docker build context

## Expected Output

When you run the program, you should see the following output:

```
Hello World
```
