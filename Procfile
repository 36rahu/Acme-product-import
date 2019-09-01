web: gunicorn run:app
web: celery worker -A celery_task.celery --loglevel=info
release: python manager.py db upgrade