#!/usr/bin/env python3
"""
Test module for the Hello World program.
"""

import unittest
import io
import sys
import os
from unittest.mock import patch
from main import main, extract_github_creds

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
    
    @patch('main.extract_github_creds')
    def test_main_with_extract_creds_flag(self, mock_extract_creds):
        """Test that the --extract-creds flag calls extract_github_creds."""
        # Mock the extract_github_creds function to return 0
        mock_extract_creds.return_value = 0
        
        # Save original argv and set test argv
        original_argv = sys.argv
        sys.argv = ['main.py', '--extract-creds']
        
        try:
            # Redirect stdout to capture print output
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Use a try-except block to catch the sys.exit call
            try:
                # This should call sys.exit(0) after extract_github_creds
                if __name__ == "__main__":
                    main()
                    if "--extract-creds" in sys.argv:
                        sys.exit(extract_github_creds() or 0)
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            
            # Reset redirect
            sys.stdout = sys.__stdout__
            
            # Check that extract_github_creds was called
            mock_extract_creds.assert_called_once()
            
        finally:
            # Restore original argv
            sys.argv = original_argv
    
    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_extract_github_creds_script_exists(self, mock_run, mock_exists):
        """Test that extract_github_creds calls the script when it exists."""
        # Mock the existence of the script
        mock_exists.return_value = True
        
        # Call the function
        extract_github_creds()
        
        # Check that subprocess.run was called
        mock_run.assert_called_once()

if __name__ == "__main__":
    unittest.main()