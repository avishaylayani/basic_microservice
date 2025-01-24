#!/bin/bash

# --------------------------------------------------------------------------------------------
# This Script sets up a Poetry environment, installs dependencies, and runs pytest on the Details_App project.
# Author: Avishay Layani
# set -x          # Enable debug mode
set -o errexit  # Exit on any command failing 
set -o pipefail # Return non-zero status if any part of a pipeline fails
# --------------------------------------------------------------------------------------------

## Installing poetry and pytest 
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3-poetry python3-pytest python3-dev

# Install project dependencies into the Poetry environment
poetry lock [--no-update]
poetry install
# Run pytest and save the results to the markdown file
pytest test.py
