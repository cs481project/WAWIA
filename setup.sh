#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install django
pip install django[argon2]
python manage.py migrate