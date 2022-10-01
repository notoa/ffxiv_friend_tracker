#!/usr/bin/env bash

# To run: source virtual_env.sh

set -e
set -u

# Create virtual python environment
if [ ! -d .venv ]; then
    python_version=$(python3 -c "from platform import python_version; print(python_version());")
    python3 -m virtualenv .venv --prompt="$python_version xiv"
fi

# Install from pipfile
pipenv install --dev --skip-lock

# Activate Python
if [ -f .venv/Scripts/activate ]; then
    echo "Activating Windows"
    source .venv/Scripts/activate
else
    echo "Activating Linux"
    source .venv/bin/activate
fi

set +u
set +e
