# import os
# import logging
# from celery import Celery
# from celery.signals import after_setup_logger
#
# from django.conf import settings
# from django.core import management
# # this code copied from manage.py
# # set the default Django settings module for the 'celery' app.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
#
# # you can change the name here
# app = Celery("main")
#
# # read config from Django settings, the CELERY namespace would make celery
# # config keys has `CELERY` prefix
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # discover and load tasks.py in django apps
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#
# @app.task
# def reload_indexes():
#     management.call_command('search_index', '--rebuild', '-f')
#
#
# @after_setup_logger.connect()
# def on_after_setup_logger(logger, **kwargs):
#     formatter = logger.handlers[0].formatter
#     file_handler = logging.FileHandler('celery.log')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)