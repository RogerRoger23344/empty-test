#!/bin/bash
# Script to create a creds.txt file with GitHub Actions secrets and variables

# Display usage information
function show_usage {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help message and exit"
    echo "  -t, --token     GitHub token (if not provided, will use GITHUB_TOKEN environment variable)"
    echo "  -r, --repo      Repository in the format 'owner/repo' (if not provided, will try to determine from git)"
    echo "  -o, --output    Output file path (default: creds.txt)"
    echo ""
    echo "Example:"
    echo "  $0 --token your_github_token --repo owner/repo --output /path/to/output.txt"
    echo ""
}

# Parse command-line arguments
TOKEN=""
REPO=""
OUTPUT="creds.txt"

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_usage
            exit 0
            ;;
        -t|--token)
            TOKEN="$2"
            shift
            shift
            ;;
        -r|--repo)
            REPO="$2"
            shift
            shift
            ;;
        -o|--output)
            OUTPUT="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if the requests library is installed
if ! python3 -c "import requests" &> /dev/null; then
    echo "Error: Python requests library is required but not installed."
    echo "Please install it using: pip install requests"
    exit 1
fi

# Set the GitHub token as an environment variable if provided
if [ -n "$TOKEN" ]; then
    export GITHUB_TOKEN="$TOKEN"
fi

# Check if the GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Warning: GITHUB_TOKEN environment variable is not set."
    echo "Using the demonstration script instead of the actual API."
    echo ""
    python3 create_creds_file.py
else
    # Build the command
    CMD="python3 extract_creds.py"
    
    if [ -n "$REPO" ]; then
        CMD="$CMD --repo $REPO"
    fi
    
    if [ -n "$OUTPUT" ]; then
        CMD="$CMD --output $OUTPUT"
    fi
    
    # Run the command
    echo "Running: $CMD"
    $CMD
fi

# Check if the file was created
if [ -f "$OUTPUT" ]; then
    echo ""
    echo "File created successfully: $OUTPUT"
    echo ""
    echo "Contents of $OUTPUT:"
    cat "$OUTPUT"
else
    echo ""
    echo "Error: Failed to create $OUTPUT"
    exit 1
fi