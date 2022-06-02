import logging
import os
import ssl

from celery import Celery
from celery.signals import after_setup_logger
from django.core import management

from main import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery("main")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
#
app.conf.update(BROKER_URL=settings.CELERY_BROKER_URL,
                CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND,
                broker_use_ssl = {
                        'ssl_cert_reqs': ssl.CERT_NONE
                    },
                redis_backend_use_ssl = {
                    'ssl_cert_reqs': ssl.CERT_NONE
                }
                )


@app.task
def reload_indexes():
    management.call_command('search_index', '--rebuild', '-f')


@after_setup_logger.connect()
def on_after_setup_logger(logger, **kwargs):
    formatter = logger.handlers[0].formatter
    file_handler = logging.FileHandler('celery.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)