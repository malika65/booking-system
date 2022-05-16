.listen(process.env.PORT || 5000)
web: gunicorn main.wsgi --log-file -
web: python manage.py collectstatic --noinput
web: python manage.py runserver 0.0.0.0:$PORT --noreload