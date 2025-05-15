#!/usr/bin/env python3
"""
Test module for the Hello World program.
"""

import unittest
import io
import sys
from main import main

class TestHelloWorld(unittest.TestCase):
    """Test case for the Hello World program."""
    
    def test_main_output(self):
        """Test that the main function prints 'Hello World'."""
        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Check if the output is as expected
        self.assertEqual(captured_output.getvalue().strip(), "Hello World")

if __name__ == "__main__":
    unittest.main()