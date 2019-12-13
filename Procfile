release: python manage.py makemigrations && python manage.py migrate
web: gunicorn fusion.wsgi:application --log-file - --log-level debug
