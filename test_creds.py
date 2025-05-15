#!/usr/bin/env python3
"""
Test module for verifying the creds.txt file.
"""

import unittest
import os

class TestCreds(unittest.TestCase):
    """Test case for the creds.txt file."""
    
    def test_creds_file_exists(self):
        """Test that the creds.txt file exists."""
        self.assertTrue(os.path.isfile('creds.txt'), "creds.txt should exist")
    
    def test_creds_file_content(self):
        """Test that the creds.txt file has the expected sections."""
        with open('creds.txt', 'r') as f:
            content = f.read()
        
        # Check for required sections
        self.assertIn("# GitHub Actions Secrets and Variables", content,
                     "creds.txt should have a title")
        self.assertIn("## Secrets", content,
                     "creds.txt should have a Secrets section")
        self.assertIn("## Variables", content,
                     "creds.txt should have a Variables section")
        
        # Check for some expected placeholder variables
        self.assertIn("SECRET_TOKEN=", content,
                     "creds.txt should include SECRET_TOKEN placeholder")
        self.assertIn("API_KEY=", content,
                     "creds.txt should include API_KEY placeholder")
        self.assertIn("ENVIRONMENT=", content,
                     "creds.txt should include ENVIRONMENT placeholder")

if __name__ == "__main__":
    unittest.main()