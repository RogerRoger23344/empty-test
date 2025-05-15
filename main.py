#!/usr/bin/env python3
"""
A simple Hello World program with GitHub credentials extraction functionality.
"""

import os
import sys
import subprocess
from typing import Optional


def main():
    """
    Main function that prints 'Hello World' to the console.
    """
    print("Hello World")


def extract_github_creds() -> Optional[int]:
    """
    Extract GitHub credentials and save them to creds.txt.
    
    Returns:
        Optional[int]: Return code from the github_creds.py script, or None if execution failed
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "github_creds.py")
    
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found", file=sys.stderr)
        return None
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )
        
        # Print output from the script
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
        return result.returncode
    except subprocess.SubprocessError as e:
        print(f"Error executing {script_path}: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    main()
    
    # Check if --extract-creds flag is provided
    if "--extract-creds" in sys.argv:
        sys.exit(extract_github_creds() or 0)