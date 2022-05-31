import os
import logging
import ssl

from celery import Celery
from celery.signals import after_setup_logger

from django.conf import settings
from django.core import management
# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# you can change the name here
# app = Celery("main")
app = Celery("main")

# print(f'connected to celery using broker: {settings.CELERY_BROKER_URL} and backend: {settings.CELERY_RESULT_BACKEND}')
# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py in django apps
app.autodiscover_tasks()
#
app.conf.update(BROKER_URL='rediss://:p2c97d946f1f1a0246db67f32f70ec89435736f51dffdcf9f7db96dcdcb16ca3c@ec2-3-251-43-118.eu-west-1.compute.amazonaws.com:25650',
                CELERY_RESULT_BACKEND='rediss://:p2c97d946f1f1a0246db67f32f70ec89435736f51dffdcf9f7db96dcdcb16ca3c@ec2-3-251-43-118.eu-west-1.compute.amazonaws.com:25650',
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