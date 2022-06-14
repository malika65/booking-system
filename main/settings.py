"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse
from django.contrib import admin

from celery.schedules import crontab
import dj_database_url
from corsheaders.defaults import default_headers
import cloudinary


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ["PATH"] = ''
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-l0)5n^%a%9ck*!pwkk=q7szp+_w%j5(ydn(e=1inhqw@wj#bo0'
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = ['https://silk-travel.herokuapp.com']

# CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect

CORS_ALLOWED_ORIGIN_REGEXES = [
    'https://silkway.bf.kg',
]

CORS_ALLOWED_ORIGINS = [
    "http://silk-travel.herokuapp.com",
    "https://silk-travel.herokuapp.com",
    "https://silkway.bf.kg",
    "https://silkway.bf.kg",
]

# CORS_ALLOW_HEADERS = [
#     'Access-Control-Allow-Origin',
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# ]

CORS_ORIGIN_WHITELIST = [
    'https://silkway.bf.kg',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'https://silkway.bf.kg',
]

AUTH_USER_MODEL = 'authe.User'

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_elasticsearch_dsl',
    'django.contrib.staticfiles',
    'cloudinary',
    'smart_selects',
    'corsheaders',
    'rest_framework',
    'rest_framework_api_key',
    'drf_yasg',
    'booking_system.apps.BookingSystemConfig',
    'authe.apps.AutheConfig',
    'django_extensions',
    'search.apps.SearchConfig',

]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ES_URL = os.environ['ES_URL']

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ES_URL,
    },
}

JQUERY_URL = False

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_SSL_REDIRECT = False


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'main.urls'

SWAGGER_SETTINGS = {
    'LOGIN_URL': '/admin/login',
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey', 
            'in': 'header',
            'name': 'Authorization'
            },
    },
    'JSON_EDITOR': True,
    'SHOW_REQUEST_HEADERS': True,
    'OPERATIONS_SORTER': 'alpha',
    'PERSIST_AUTH': True,
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework_api_key.permissions.HasAPIKey',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25
}

# Configure the JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'build/static'),
#     os.path.join(BASE_DIR, 'static'),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field


EMAIL_FROM = os.environ['EMAIL_FROM']
EMAIL_BCC = 'Qualle'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SERVER_EMAIL = os.environ['SERVER_EMAIL']


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}


LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'main.translation'

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


db_from_env = dj_database_url.config(default=os.environ['DATABASE_URL'])
DATABASES['default'].update(db_from_env)


CELERY_BROKER_URL = os.environ['REDIS_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

CELERY_BEAT_SCHEDULE = {
    'queue_every_five_mins': {
        'task': 'polls.tasks.query_every_five_mins',
        'schedule': crontab(minute=5),
    },
}

CURRENCY_RATES_URL = os.environ['CURRENCY_RATES_URL']
CURRENCY_RATES_API_KEY = os.environ['CURRENCY_RATES_API_KEY']


CACHE_TTL = 60 * 240

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION':  os.environ['REDIS_URL'],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'ssl_cert_reqs': None},
        }
    }
}

ADMIN_ORDERING = (
    ('authe', [
        'User',
        'ConfirmCode',

    ]),
    ('booking_system', [
        'Hotel',
        'Booking',
        'Category',
        'FacilitiesAndServicesHotels',
        'HotelCategoryStars',
        'AdditionalService',
        'ChildService',
        'Room',
        'FacilitiesAndServicesRooms',
        'Characteristics',
        'FoodCategory',
        'AdditionalService',
        'Country',
        'HotelImage'
    ]),
    ('rest_framework_api_key', [
        'APIKey'
    ])
)


# Creating a sort function
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in ADMIN_ORDERING:
        app = app_dict[app_name]

        app['models'].sort(key=lambda x: object_list.index(x['object_name']))
        yield app


# Covering django.contrib.admin.AdminSite.get_app_list

admin.AdminSite.get_app_list = get_app_list

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUD_NAME'],
    'API_KEY': os.environ['API_KEY'],
    'API_SECRET': os.environ['API_SECRET'],
}

cloudinary.config(
    cloud_name=os.environ['CLOUD_NAME'],
    api_key=os.environ['API_KEY'],
    api_secret=os.environ['API_SECRET'],
    use_filename=True
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'