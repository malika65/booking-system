release: python manage.py migrate
.listen(process.env.PORT || 5000)
worker: python manage.py collectstatic --noinput
web: python manage.py runserver 0.0.0.0:$PORT --noreload
worker: celery -A main worker -l info --concurrency 2
