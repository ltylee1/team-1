#!/bin/bash
python manage.py runserver --insecure 0.0.0.0:8000 >> output.log &
