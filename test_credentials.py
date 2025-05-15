#!/usr/bin/env python3
"""
Test module for the credentials functionality.
"""

import unittest
import os
import tempfile
from main import read_credentials

class TestCredentials(unittest.TestCase):
    """Test case for the credentials functionality."""
    
    def test_creds_file_exists(self):
        """Test that the creds.txt file exists at the root of the repository."""
        self.assertTrue(os.path.isfile('creds.txt'), "creds.txt should exist at the root of the repository")
    
    def test_read_credentials(self):
        """Test that the read_credentials function correctly parses the credentials file."""
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("# Test credentials file\n")
            temp_file.write("API_KEY=test_api_key\n")
            temp_file.write("SECRET_TOKEN=test_secret_token\n")
            temp_file.write("# Comment line\n")
            temp_file.write("\n")  # Empty line
            temp_file.write("DEBUG=true\n")
            temp_filename = temp_file.name
        
        try:
            # Test reading the credentials
            credentials = read_credentials(temp_filename)
            
            # Verify the credentials were read correctly
            self.assertIsNotNone(credentials, "Credentials should not be None")
            self.assertEqual(credentials.get("API_KEY"), "test_api_key")
            self.assertEqual(credentials.get("SECRET_TOKEN"), "test_secret_token")
            self.assertEqual(credentials.get("DEBUG"), "true")
            self.assertEqual(len(credentials), 3, "Should have read 3 credentials")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_read_nonexistent_file(self):
        """Test that the read_credentials function handles nonexistent files gracefully."""
        credentials = read_credentials("nonexistent_file.txt")
        self.assertIsNone(credentials, "Should return None for nonexistent files")

if __name__ == "__main__":
    unittest.main()