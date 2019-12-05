release: python manage.py makemigrations authentication property transactions
release: python manage.py migrate

web: gunicorn fusion.wsgi
worker: celery -A fusion worker -l info