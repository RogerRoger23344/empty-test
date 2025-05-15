#!/usr/bin/env python3
"""
Test module for verifying documentation.
"""

import unittest
import os
import re

class TestDocumentation(unittest.TestCase):
    """Test case for documentation verification."""
    
    def test_readme_exists(self):
        """Test that the README.md file exists."""
        self.assertTrue(os.path.isfile('README.md'), "README.md should exist")
    
    def test_readme_sections(self):
        """Test that the README.md contains all required sections."""
        required_sections = [
            "# Hello World Project",
            "## Description",
            "## Requirements",
            "## Installation",
            "## How to Run",
            "## Project Structure",
            "## Testing",
            "## Expected Output",
            "## Troubleshooting",
            "## Contributing",
            "## License",
            "## Version",
            "## Authors",
            "## Acknowledgments"
        ]
        
        with open('README.md', 'r') as f:
            content = f.read()
            
        for section in required_sections:
            self.assertIn(section, content, f"README.md should contain the section: {section}")
    
    def test_readme_content_completeness(self):
        """Test that the README.md contains comprehensive content."""
        with open('README.md', 'r') as f:
            content = f.read()
        
        # Check for code examples
        self.assertGreater(content.count('```'), 4, "README.md should contain multiple code examples")
        
        # Check for links
        self.assertGreater(len(re.findall(r'\[.*?\]\(.*?\)', content)), 0, "README.md should contain links")
        
        # Check for list items
        self.assertGreater(content.count('- '), 5, "README.md should contain multiple list items")

if __name__ == "__main__":
    unittest.main()