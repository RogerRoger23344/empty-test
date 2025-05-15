#!/usr/bin/env python3
"""
Test module for the GitHub credentials functionality.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from github_creds import (
    get_github_token,
    get_repo_info,
    get_github_secrets,
    get_github_variables,
    write_creds_to_file
)


class TestGitHubCreds(unittest.TestCase):
    """Test case for the GitHub credentials functionality."""
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    def test_get_github_token(self):
        """Test that the GitHub token is retrieved correctly."""
        token = get_github_token()
        self.assertEqual(token, "test_token")
    
    def test_get_github_token_missing(self):
        """Test that an error is raised when the GitHub token is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                get_github_token()
    
    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo"})
    def test_get_repo_info_from_env(self):
        """Test that repository information is retrieved from environment variables."""
        owner, repo = get_repo_info()
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")
    
    @patch("github_creds.subprocess.run")
    def test_get_repo_info_from_git_https(self, mock_run):
        """Test that repository information is retrieved from git config (HTTPS URL)."""
        # Mock subprocess.run to return a git HTTPS URL
        mock_process = MagicMock()
        mock_process.stdout = "https://github.com/owner/repo.git\n"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Remove environment variable to force git lookup
        with patch.dict(os.environ, {}, clear=True):
            owner, repo = get_repo_info()
            self.assertEqual(owner, "owner")
            self.assertEqual(repo, "repo")
    
    @patch("github_creds.subprocess.run")
    def test_get_repo_info_from_git_ssh(self, mock_run):
        """Test that repository information is retrieved from git config (SSH URL)."""
        # Mock subprocess.run to return a git SSH URL
        mock_process = MagicMock()
        mock_process.stdout = "git@github.com:owner/repo.git\n"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Remove environment variable to force git lookup
        with patch.dict(os.environ, {}, clear=True):
            owner, repo = get_repo_info()
            self.assertEqual(owner, "owner")
            self.assertEqual(repo, "repo")
    
    @patch("github_creds.requests.get")
    def test_get_github_secrets(self, mock_get):
        """Test that GitHub secrets are retrieved correctly."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "secrets": [
                {"name": "SECRET1"},
                {"name": "SECRET2"}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        secrets = get_github_secrets("owner", "repo", "token")
        self.assertEqual(len(secrets), 2)
        self.assertEqual(secrets[0]["name"], "SECRET1")
        self.assertEqual(secrets[1]["name"], "SECRET2")
    
    @patch("github_creds.requests.get")
    def test_get_github_variables(self, mock_get):
        """Test that GitHub variables are retrieved correctly."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "variables": [
                {"name": "VAR1", "value": "value1"},
                {"name": "VAR2", "value": "value2"}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        variables = get_github_variables("owner", "repo", "token")
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0]["name"], "VAR1")
        self.assertEqual(variables[0]["value"], "value1")
        self.assertEqual(variables[1]["name"], "VAR2")
        self.assertEqual(variables[1]["value"], "value2")
    
    def test_write_creds_to_file(self):
        """Test that credentials are written to a file correctly."""
        secrets = [
            {"name": "SECRET1"},
            {"name": "SECRET2"}
        ]
        variables = [
            {"name": "VAR1", "value": "value1"},
            {"name": "VAR2", "value": "value2"}
        ]
        
        # Use a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Write credentials to the temporary file
            write_creds_to_file(secrets, variables, temp_filename)
            
            # Read the file and check its contents
            with open(temp_filename, "r") as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), 4)
            self.assertEqual(lines[0], "SECRET1=<SECRET_VALUE_PROTECTED>\n")
            self.assertEqual(lines[1], "SECRET2=<SECRET_VALUE_PROTECTED>\n")
            self.assertEqual(lines[2], "VAR1=value1\n")
            self.assertEqual(lines[3], "VAR2=value2\n")
        
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == "__main__":
    unittest.main()