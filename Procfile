release: python manage.py migrate

web: gunicorn main.wsgi --log-file -

worker: python manage.py collectstatic --noinput
worker: python manage.py runserver 0.0.0.0:$PORT --noreload
worker: celery worker --app=booking_system.app