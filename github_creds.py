#!/usr/bin/env python3
"""
GitHub Credentials Extractor

This script extracts GitHub Actions secrets and variables from a repository
and writes them to a creds.txt file.
"""

import os
import sys
import requests
import json
from typing import Dict, List, Tuple, Optional


def get_github_token() -> Optional[str]:
    """
    Get GitHub token from environment variable.
    
    Returns:
        Optional[str]: GitHub token if available, None otherwise
    """
    return os.environ.get("GITHUB_TOKEN")


def get_repo_info() -> Tuple[Optional[str], Optional[str]]:
    """
    Get repository owner and name from environment variables or git config.
    
    Returns:
        Tuple[Optional[str], Optional[str]]: Repository owner and name
    """
    # Try to get from environment variables (common in CI environments)
    if "GITHUB_REPOSITORY" in os.environ:
        repo_full_name = os.environ["GITHUB_REPOSITORY"]
        owner, repo = repo_full_name.split("/", 1)
        return owner, repo
    
    # Try to get from git remote URL
    try:
        import subprocess
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parse GitHub URL format: https://github.com/owner/repo.git or git@github.com:owner/repo.git
        if "github.com" in remote_url:
            if remote_url.startswith("https://"):
                path = remote_url.split("github.com/")[1]
            else:  # SSH format
                path = remote_url.split("github.com:")[1]
                
            # Remove .git extension if present
            if path.endswith(".git"):
                path = path[:-4]
                
            if "/" in path:
                owner, repo = path.split("/", 1)
                return owner, repo
    except (subprocess.SubprocessError, ImportError, IndexError):
        pass
    
    return None, None


def get_github_actions_secrets(owner: str, repo: str, token: str) -> List[Dict]:
    """
    Get GitHub Actions secrets for a repository.
    Note: Due to GitHub's security model, we can only get secret names, not values.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str): GitHub token with appropriate permissions
        
    Returns:
        List[Dict]: List of secrets with their names
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("secrets", [])
    except requests.RequestException as e:
        print(f"Error fetching GitHub secrets: {e}", file=sys.stderr)
        return []


def get_github_actions_variables(owner: str, repo: str, token: str) -> List[Dict]:
    """
    Get GitHub Actions variables for a repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str): GitHub token with appropriate permissions
        
    Returns:
        List[Dict]: List of variables with their names and values
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/variables"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("variables", [])
    except requests.RequestException as e:
        print(f"Error fetching GitHub variables: {e}", file=sys.stderr)
        return []


def write_creds_to_file(secrets: List[Dict], variables: List[Dict]) -> bool:
    """
    Write credentials to creds.txt file.
    
    Args:
        secrets (List[Dict]): List of secrets
        variables (List[Dict]): List of variables
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open("creds.txt", "w") as f:
            # Write secrets (note: values are not available, only names)
            for secret in secrets:
                f.write(f"{secret['name']}=<SECRET_VALUE_ENCRYPTED>\n")
            
            # Write variables
            for variable in variables:
                f.write(f"{variable['name']}={variable.get('value', '<NOT_ACCESSIBLE>')}\n")
        
        return True
    except IOError as e:
        print(f"Error writing to creds.txt: {e}", file=sys.stderr)
        return False


def main():
    """
    Main function to extract GitHub Actions secrets and variables.
    """
    print("Starting GitHub credentials extraction...")
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("GitHub token not found. Please set the GITHUB_TOKEN environment variable.", file=sys.stderr)
        print("Creating empty creds.txt file as fallback...")
        with open("creds.txt", "w") as f:
            f.write("# GitHub credentials could not be accessed\n")
            f.write("# To populate this file, run this script with a valid GITHUB_TOKEN\n")
        return 1
    
    # Get repository information
    owner, repo = get_repo_info()
    if not owner or not repo:
        print("Could not determine repository owner and name.", file=sys.stderr)
        print("Creating empty creds.txt file as fallback...")
        with open("creds.txt", "w") as f:
            f.write("# GitHub repository information could not be determined\n")
            f.write("# To populate this file, run this script in a GitHub repository\n")
        return 1
    
    print(f"Repository: {owner}/{repo}")
    
    # Get secrets and variables
    secrets = get_github_actions_secrets(owner, repo, token)
    variables = get_github_actions_variables(owner, repo, token)
    
    print(f"Found {len(secrets)} secrets and {len(variables)} variables")
    
    # Write to file
    if write_creds_to_file(secrets, variables):
        print("Successfully wrote credentials to creds.txt")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())