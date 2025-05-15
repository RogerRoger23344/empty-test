#!/usr/bin/env python3
"""
Test module for verifying Docker functionality.
"""

import unittest
import subprocess
import os

class TestDocker(unittest.TestCase):
    """Test case for Docker functionality."""
    
    def test_dockerfile_exists(self):
        """Test that the Dockerfile exists."""
        self.assertTrue(os.path.isfile('Dockerfile'), "Dockerfile should exist")
    
    def test_dockerignore_exists(self):
        """Test that the .dockerignore file exists."""
        self.assertTrue(os.path.isfile('.dockerignore'), ".dockerignore should exist")
    
    def test_docker_build(self):
        """
        Test that the Docker image builds successfully.
        Note: This test requires Docker to be installed and running.
        Skip this test if you don't have Docker available.
        """
        try:
            # Check if Docker is available
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            self.skipTest("Docker is not available, skipping build test")
        
        # Try to build the Docker image
        result = subprocess.run(
            ["docker", "build", "-t", "hello-world-test", "."],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Docker build failed: {result.stderr}")
    
    def test_docker_run_main(self):
        """
        Test that the Docker container runs the main.py script by default.
        Note: This test requires Docker to be installed and running.
        Skip this test if you don't have Docker available.
        """
        try:
            # Check if Docker is available
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            self.skipTest("Docker is not available, skipping run test")
        
        # Build the Docker image if it doesn't exist
        try:
            subprocess.run(
                ["docker", "image", "inspect", "hello-world-test"],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                ["docker", "build", "-t", "hello-world-test", "."],
                check=True,
                capture_output=True
            )
        
        # Run the Docker container
        result = subprocess.run(
            ["docker", "run", "--rm", "hello-world-test"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Docker run failed: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "Hello World", "Docker container should output 'Hello World'")
    
    def test_docker_run_create_creds_file(self):
        """
        Test that the Docker container can run the create_creds_file.py script.
        Note: This test requires Docker to be installed and running.
        Skip this test if you don't have Docker available.
        """
        try:
            # Check if Docker is available
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            self.skipTest("Docker is not available, skipping run test")
        
        # Build the Docker image if it doesn't exist
        try:
            subprocess.run(
                ["docker", "image", "inspect", "hello-world-test"],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                ["docker", "build", "-t", "hello-world-test", "."],
                check=True,
                capture_output=True
            )
        
        # Run the Docker container with the create_creds_file.py script
        result = subprocess.run(
            ["docker", "run", "--rm", "hello-world-test", "create_creds_file.py"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Docker run failed: {result.stderr}")
        self.assertIn("Successfully created creds.txt file", result.stdout, "Docker container should create creds.txt file")

if __name__ == "__main__":
    unittest.main()