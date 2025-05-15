#!/usr/bin/env python3
"""
Test module for verifying the example.html file.
"""

import unittest
import os

class TestExampleHtml(unittest.TestCase):
    """Test case for the example.html file."""
    
    def test_example_html_exists(self):
        """Test that the example.html file exists."""
        self.assertTrue(os.path.isfile('example.html'), "example.html should exist")
    
    def test_example_html_content(self):
        """Test that the example.html file contains expected placeholder content."""
        with open('example.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholder indicators
        self.assertIn("placeholder", content.lower(), 
                     "example.html should contain placeholder text")
        
        # Check for Amazon reference
        self.assertIn("amazon.com", content.lower(), 
                     "example.html should reference amazon.com")

if __name__ == "__main__":
    unittest.main()