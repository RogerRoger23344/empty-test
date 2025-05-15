#!/usr/bin/env python3
"""
Script to create a creds.txt file with GitHub Actions secrets and variables.

This script demonstrates how to use the github_creds module to create a creds.txt file
containing GitHub Actions secrets and variables from a repository.
"""

import os
import sys
from github_creds import (
    get_github_token,
    get_repo_info,
    get_github_secrets,
    get_github_variables,
    write_creds_to_file
)


def main():
    """
    Main function to create a creds.txt file with GitHub Actions secrets and variables.
    """
    try:
        print("Creating creds.txt file with GitHub Actions secrets and variables...")
        
        # Check if GITHUB_TOKEN environment variable is set
        if "GITHUB_TOKEN" not in os.environ:
            print("Warning: GITHUB_TOKEN environment variable is not set.")
            print("Using a placeholder token for demonstration purposes.")
            print("In a real environment, you would need to set this variable.")
            os.environ["GITHUB_TOKEN"] = "demo_token"
        
        # Get GitHub token
        token = get_github_token()
        
        try:
            # Try to get repository information
            owner, repo = get_repo_info()
            print(f"Repository: {owner}/{repo}")
        except ValueError:
            # If repository information cannot be determined, use placeholder values
            print("Warning: Could not determine repository information.")
            print("Using placeholder values for demonstration purposes.")
            owner = "demo_owner"
            repo = "demo_repo"
        
        # In a real environment, we would call the GitHub API to get secrets and variables
        # For demonstration purposes, we'll create some sample data
        print("Note: Using sample data for demonstration purposes.")
        print("In a real environment, this would call the GitHub API.")
        
        # Sample secrets (in reality, these would come from the GitHub API)
        secrets = [
            {"name": "API_KEY"},
            {"name": "DATABASE_PASSWORD"},
            {"name": "JWT_SECRET"}
        ]
        print(f"Found {len(secrets)} secrets")
        
        # Sample variables (in reality, these would come from the GitHub API)
        variables = [
            {"name": "DATABASE_URL", "value": "postgres://user:password@localhost:5432/db"},
            {"name": "ENVIRONMENT", "value": "production"},
            {"name": "DEBUG", "value": "false"}
        ]
        print(f"Found {len(variables)} variables")
        
        # Write to creds.txt file
        write_creds_to_file(secrets, variables, "creds.txt")
        print("Successfully created creds.txt file")
        
        # Display the contents of the file
        print("\nContents of creds.txt:")
        with open("creds.txt", "r") as f:
            print(f.read())
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())