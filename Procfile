web:      bin/python lavender/manage.py run_gunicorn -b 0.0.0.0:\$PORT -w 3
worker:   bin/python lavender/manage.py celeryd -E -B --loglevel=INFO