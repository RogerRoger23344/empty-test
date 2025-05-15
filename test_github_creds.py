#!/usr/bin/env python3
"""
Test module for GitHub credentials extraction functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from main import extract_github_creds


class TestGitHubCreds(unittest.TestCase):
    """Test case for GitHub credentials extraction functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_extract_github_creds_success(self, mock_exists, mock_run):
        """Test successful execution of GitHub credentials extraction."""
        # Mock the existence of the script
        mock_exists.return_value = True
        
        # Mock successful execution of the script
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Successfully extracted GitHub credentials"
        mock_process.stderr = ""
        mock_run.return_value = mock_process
        
        # Call the function
        result = extract_github_creds()
        
        # Verify the result
        self.assertEqual(result, 0)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_extract_github_creds_script_not_found(self, mock_exists, mock_run):
        """Test handling of missing script file."""
        # Mock the non-existence of the script
        mock_exists.return_value = False
        
        # Call the function
        result = extract_github_creds()
        
        # Verify the result
        self.assertIsNone(result)
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_extract_github_creds_execution_error(self, mock_exists, mock_run):
        """Test handling of script execution error."""
        # Mock the existence of the script
        mock_exists.return_value = True
        
        # Mock execution error
        mock_run.side_effect = Exception("Execution error")
        
        # Call the function
        result = extract_github_creds()
        
        # Verify the result
        self.assertIsNone(result)
    
    @patch('subprocess.run')
    @patch('os.path.exists')
    def test_extract_github_creds_script_error(self, mock_exists, mock_run):
        """Test handling of script returning an error code."""
        # Mock the existence of the script
        mock_exists.return_value = True
        
        # Mock script execution with error code
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = ""
        mock_process.stderr = "Error: Could not access GitHub API"
        mock_run.return_value = mock_process
        
        # Call the function
        result = extract_github_creds()
        
        # Verify the result
        self.assertEqual(result, 1)
        mock_run.assert_called_once()
    
    def test_creds_file_creation(self):
        """
        Test that the creds.txt file can be created.
        This is a basic file creation test, not testing the actual API calls.
        """
        # Create a simple creds.txt file
        with open("creds.txt", "w") as f:
            f.write("TEST_SECRET=test_value\n")
            f.write("API_KEY=dummy_key\n")
        
        # Verify the file exists
        self.assertTrue(os.path.exists("creds.txt"))
        
        # Verify the content
        with open("creds.txt", "r") as f:
            content = f.read()
        
        self.assertIn("TEST_SECRET=test_value", content)
        self.assertIn("API_KEY=dummy_key", content)


if __name__ == "__main__":
    unittest.main()