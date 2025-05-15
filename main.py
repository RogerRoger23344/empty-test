#!/usr/bin/env python3
"""
A simple Hello World program with credential reading capability.
"""
import os

def main():
    """
    Main function that prints 'Hello World' to the console.
    """
    print("Hello World")

def read_credentials(filepath="creds.txt"):
    """
    Read credentials from the creds.txt file.
    
    Args:
        filepath (str): Path to the credentials file
        
    Returns:
        dict: Dictionary of credentials or None if file doesn't exist
    """
    if not os.path.exists(filepath):
        print(f"Credentials file not found: {filepath}")
        return None
    
    credentials = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse key-value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading credentials: {e}")
        return None
    
    return credentials

if __name__ == "__main__":
    main()