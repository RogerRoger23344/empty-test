# Testing Documentation

This document outlines the testing procedures for the Hello World application.

## Unit Tests

The project includes unit tests to verify the core functionality of the application.

### Running Unit Tests

To run the unit tests, execute the following command from the project root:

```bash
python -m unittest test_main.py
```

### Test Coverage

The unit tests cover:

- Verifying that the `main()` function correctly outputs "Hello World"

## Docker Tests

The project also includes tests to verify Docker functionality.

### Running Docker Tests

To run the Docker tests, execute the following command from the project root:

```bash
python -m unittest test_docker.py
```

Note: Docker tests require Docker to be installed and running on your system. Tests will be skipped automatically if Docker is not available.

### Docker Test Coverage

The Docker tests cover:

- Verifying that the Dockerfile exists
- Verifying that the .dockerignore file exists
- Verifying that the Docker image builds successfully

## Manual Testing

For manual testing:

1. Run the application directly:
   ```bash
   python main.py
   ```
   Expected output: `Hello World`

2. Run the application using Docker:
   ```bash
   docker build -t hello-world .
   docker run --rm hello-world
   ```
   Expected output: `Hello World`

## Continuous Integration

For CI/CD pipelines, you can run all tests with:

```bash
python -m unittest discover
```

This will discover and run all test files in the project.