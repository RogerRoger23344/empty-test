#!/usr/bin/env python3
"""
Script to access GitHub Actions secrets and variables and write them to a file.

This script uses the GitHub API to retrieve Actions secrets and variables
from the repository's metadata and writes them to a creds.txt file.
"""

import os
import sys
import requests
import json
from typing import Dict, List, Tuple, Optional


def get_github_token() -> str:
    """
    Get GitHub token from environment variable.
    
    Returns:
        str: GitHub token
    
    Raises:
        ValueError: If GitHub token is not found in environment variables
    """
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "GitHub token not found. Please set the GITHUB_TOKEN environment variable."
        )
    return token


def get_repo_info() -> Tuple[str, str]:
    """
    Get repository owner and name from environment variables or git config.
    
    Returns:
        Tuple[str, str]: Repository owner and name
    
    Raises:
        ValueError: If repository information cannot be determined
    """
    # Try to get from GITHUB_REPOSITORY environment variable (available in GitHub Actions)
    github_repo = os.environ.get("GITHUB_REPOSITORY")
    if github_repo and "/" in github_repo:
        owner, repo = github_repo.split("/", 1)
        return owner, repo
    
    # If not in GitHub Actions, try to get from git remote
    try:
        import subprocess
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parse GitHub URL to extract owner and repo
        if "github.com" in remote_url:
            if remote_url.startswith("git@github.com:"):
                # SSH URL format: git@github.com:owner/repo.git
                path = remote_url.split("git@github.com:")[1]
            elif remote_url.startswith("https://github.com/"):
                # HTTPS URL format: https://github.com/owner/repo.git
                path = remote_url.split("https://github.com/")[1]
            else:
                raise ValueError(f"Unsupported GitHub URL format: {remote_url}")
            
            # Remove .git extension if present
            if path.endswith(".git"):
                path = path[:-4]
            
            if "/" in path:
                owner, repo = path.split("/", 1)
                return owner, repo
    except (subprocess.SubprocessError, ImportError, IndexError, ValueError) as e:
        print(f"Error determining repository from git: {e}")
    
    raise ValueError(
        "Could not determine repository information. "
        "Please set the GITHUB_REPOSITORY environment variable "
        "or run this script from a valid git repository."
    )


def get_github_secrets(owner: str, repo: str, token: str) -> List[Dict]:
    """
    Get GitHub Actions secrets for a repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str): GitHub token
    
    Returns:
        List[Dict]: List of secrets
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json().get("secrets", [])


def get_github_variables(owner: str, repo: str, token: str) -> List[Dict]:
    """
    Get GitHub Actions variables for a repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str): GitHub token
    
    Returns:
        List[Dict]: List of variables
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/variables"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json().get("variables", [])


def write_creds_to_file(secrets: List[Dict], variables: List[Dict], filename: str = "creds.txt") -> None:
    """
    Write GitHub Actions secrets and variables to a file.
    
    Args:
        secrets (List[Dict]): List of secrets
        variables (List[Dict]): List of variables
        filename (str, optional): Output filename. Defaults to "creds.txt".
    """
    with open(filename, "w") as f:
        # Write secrets
        for secret in secrets:
            # Note: GitHub API doesn't return secret values for security reasons
            # We can only list the names of secrets
            f.write(f"{secret['name']}=<SECRET_VALUE_PROTECTED>\n")
        
        # Write variables
        for variable in variables:
            f.write(f"{variable['name']}={variable['value']}\n")


def main() -> None:
    """
    Main function to retrieve GitHub Actions secrets and variables and write them to a file.
    """
    try:
        # Get GitHub token
        token = get_github_token()
        
        # Get repository information
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
        write_creds_to_file(secrets, variables)
        print(f"Successfully wrote credentials to creds.txt")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()