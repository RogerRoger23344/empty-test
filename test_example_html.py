#!/usr/bin/env python3
"""
Test module for verifying the existence of example.html file.
"""

import unittest
import os

class TestExampleHTML(unittest.TestCase):
    """Test case for example.html file."""
    
    def test_example_html_exists(self):
        """Test that the example.html file exists."""
        self.assertTrue(os.path.isfile('example.html'), "example.html should exist")
    
    def test_example_html_content(self):
        """Test that the example.html file contains expected content."""
        with open('example.html', 'r') as file:
            content = file.read()
            self.assertIn("Example Domain", content, 
                         "example.html should contain 'Example Domain'")
            self.assertIn("<!doctype html>", content.lower(), 
                         "example.html should be an HTML document")

if __name__ == "__main__":
    unittest.main()