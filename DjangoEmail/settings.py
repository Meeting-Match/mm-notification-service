"""
Django settings for DjangoEmail project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)3(se98f0xy$myl2sficy8lh^!=9(46rx%41(w!#a(%tvl=-zy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'notification-service-env.eba-37gex8hp.us-east-2.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1',
    '18.191.54.221',
    '3.15.225.226',
    '3.144.254.242'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainApp',
    'rest_framework',
]

MIDDLEWARE = [
    'DjangoEmail.middleware.CorrelationIdMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoEmail.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DjangoEmail.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

env = environ.Env()
environ.Env.read_env()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env('DB_NAME'),
        "USER": env('DB_USER'),
        "PASSWORD": env('DB_PASSWORD'),
        "HOST": env('DB_HOST'),
        "PORT": env('DB_PORT'),
        "OPTIONS": {
            "ssl": {
                "ca": env('DB_CA'),
            }
        }
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# send email funtionality

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dbuserdbuser588@gmail.com'
EMAIL_HOST_PASSWORD = 'wzhy ucbi tilg uxjx'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 300  # in seconds


'''#Add in function later
EMAIL_HOST = '<smtp.yourserver.com>'
EMAIL_HOST_USER = 'your@djangoapp.com'
EMAIL_HOST_PASSWORD ='your password'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_TIMEOUT = 300 # in seconds
DEFAULT_FROM_EMAIL = 'sender name <your@djangoapp.com>'
'''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'add_correlation_id': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: setattr(record, 'correlation_id', getattr(record, 'correlation_id', 'N/A')) or True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message} {correlation_id}',
            'style': '{',
        },
        'default': {
            'format': '{levelname} {asctime} {message} {correlation_id}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['add_correlation_id'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'notification': {  # Logger for your app
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {  # Added to handle logs from unnamed loggers
        'handlers': ['console'],
        'level': 'INFO',
    },
}