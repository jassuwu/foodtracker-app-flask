#!/usr/bin/env bash
# exit on error
set -o errexit

# requirements/python modules
pip install --upgrade pip
pip install -r requirements.txt

# init flask db from Flask-Migrate
flask db stamp head
flask db migrate
flask db upgrade