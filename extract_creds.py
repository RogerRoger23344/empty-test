#!/usr/bin/env python3
"""
Command-line interface for extracting GitHub Actions secrets and variables.

This script provides a simple command-line interface for extracting GitHub Actions
secrets and variables from a repository and writing them to a file.
"""

import argparse
import os
import sys
from github_creds import get_github_token, get_repo_info, get_github_secrets, get_github_variables, write_creds_to_file


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract GitHub Actions secrets and variables from a repository."
    )
    parser.add_argument(
        "--output", "-o",
        default="creds.txt",
        help="Output file path (default: creds.txt)"
    )
    parser.add_argument(
        "--token", "-t",
        help="GitHub token (if not provided, will use GITHUB_TOKEN environment variable)"
    )
    parser.add_argument(
        "--repo", "-r",
        help="Repository in the format 'owner/repo' (if not provided, will try to determine from environment or git)"
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    try:
        # Get GitHub token
        if args.token:
            token = args.token
            os.environ["GITHUB_TOKEN"] = token
        else:
            token = get_github_token()
        
        # Get repository information
        if args.repo and "/" in args.repo:
            owner, repo = args.repo.split("/", 1)
        else:
            owner, repo = get_repo_info()
        
        print(f"Repository: {owner}/{repo}")
        
        # Get GitHub Actions secrets and variables
        print("Retrieving GitHub Actions secrets...")
        secrets = get_github_secrets(owner, repo, token)
        print(f"Found {len(secrets)} secrets")
        
        print("Retrieving GitHub Actions variables...")
        variables = get_github_variables(owner, repo, token)
        print(f"Found {len(variables)} variables")
        
        # Write to file
        write_creds_to_file(secrets, variables, args.output)
        print(f"Successfully wrote credentials to {args.output}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())