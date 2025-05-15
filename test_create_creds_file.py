#!/usr/bin/env python3
"""
Test module for the create_creds_file.py script.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile
import shutil


class TestCreateCredsFile(unittest.TestCase):
    """Test case for the create_creds_file.py script."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Add the parent directory to sys.path to import the module
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
    
    def tearDown(self):
        """Clean up the test environment."""
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
        
        # Remove the parent directory from sys.path
        sys.path.pop(0)
    
    @patch("create_creds_file.get_github_token")
    @patch("create_creds_file.get_repo_info")
    @patch("create_creds_file.write_creds_to_file")
    def test_main_success(self, mock_write, mock_get_repo, mock_get_token):
        """Test that the main function runs successfully."""
        # Mock the functions
        mock_get_token.return_value = "test_token"
        mock_get_repo.return_value = ("test_owner", "test_repo")
        
        # Import the module
        import create_creds_file
        
        # Run the main function
        result = create_creds_file.main()
        
        # Check that the function returned success
        self.assertEqual(result, 0)
        
        # Check that the functions were called
        mock_get_token.assert_called_once()
        mock_get_repo.assert_called_once()
        mock_write.assert_called_once()
        
        # Check that write_creds_to_file was called with the correct arguments
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 3)
        self.assertEqual(len(args[0]), 3)  # 3 secrets
        self.assertEqual(len(args[1]), 3)  # 3 variables
        self.assertEqual(args[2], "creds.txt")  # Output file
    
    @patch("create_creds_file.get_github_token")
    @patch("create_creds_file.get_repo_info")
    def test_main_with_real_file_creation(self, mock_get_repo, mock_get_token):
        """Test that the main function creates a real file."""
        # Mock the functions
        mock_get_token.return_value = "test_token"
        mock_get_repo.return_value = ("test_owner", "test_repo")
        
        # Import the module
        import create_creds_file
        
        # Run the main function
        result = create_creds_file.main()
        
        # Check that the function returned success
        self.assertEqual(result, 0)
        
        # Check that the file was created
        self.assertTrue(os.path.exists("creds.txt"))
        
        # Check the contents of the file
        with open("creds.txt", "r") as f:
            content = f.read()
        
        # Check that the file contains the expected number of lines
        lines = content.strip().split("\n")
        self.assertEqual(len(lines), 6)  # 3 secrets + 3 variables
        
        # Check that the file contains the expected secrets and variables
        self.assertIn("API_KEY=<SECRET_VALUE_PROTECTED>", content)
        self.assertIn("DATABASE_PASSWORD=<SECRET_VALUE_PROTECTED>", content)
        self.assertIn("JWT_SECRET=<SECRET_VALUE_PROTECTED>", content)
        self.assertIn("DATABASE_URL=postgres://user:password@localhost:5432/db", content)
        self.assertIn("ENVIRONMENT=production", content)
        self.assertIn("DEBUG=false", content)
    
    @patch("create_creds_file.get_github_token")
    @patch("create_creds_file.get_repo_info")
    def test_main_with_error(self, mock_get_repo, mock_get_token):
        """Test that the main function handles errors correctly."""
        # Mock the functions to raise an exception
        mock_get_token.side_effect = ValueError("Test error")
        
        # Import the module
        import create_creds_file
        
        # Run the main function
        result = create_creds_file.main()
        
        # Check that the function returned an error
        self.assertEqual(result, 1)
        
        # Check that the file was not created
        self.assertFalse(os.path.exists("creds.txt"))


if __name__ == "__main__":
    unittest.main()