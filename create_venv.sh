#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script is meant to be sourced, not executed directly."
    return 1
fi

if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Installing..."
    python3 -m pip install virtualenv
fi

python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

if [ -f requirements.txt ]; then
    echo "Installing packages from requirements.txt..."
    python3 -m pip install -r requirements.txt
fi

echo "Virtual environment 'venv' created and activated. You can deactivate it using 'deactivate'."
