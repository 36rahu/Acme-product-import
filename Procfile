web: gunicorn run:app
celery worker -A celery_task.celery --loglevel=info
release: python manage.py db upgrade