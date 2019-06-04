#!/bin/sh

pip install -r requirements.txt

cd othello
python manage.py runserver 0.0.0.0:8000
