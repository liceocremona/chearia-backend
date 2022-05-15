#!/bin/bash
. /home/chearia/chearia-repo-backend/client/backend/venv/bin/activate &&  /home/chearia/chearia-repo-backend/client/backend/venv/bin/gunicorn --preload --workers 3 --env "SCRIPT_NAME=/v1" --bind unix:chearia_backend.sock -m 777 wsgi:app
