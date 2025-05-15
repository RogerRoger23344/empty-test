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

if __name__ == "__main__":
    unittest.main()