"""
Django settings for web_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import random
import string
from pathlib import Path

from dotenv import load_dotenv

from .template import  THEME_LAYOUT_DIR, THEME_VARIABLES

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Update secret key in .env file and .env.prod file
# SECRET_KEY = os.environ.get("SECRET_KEY", default='')

# SECURITY WARNING: keep the secret key used in production secret!
# If using the .env file for SECRET_KEY then comment below random SECRET_KEY generation code.
SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY_COHERE = os.environ.get("SECRET_KEY_COHERE")
SECRET_KEY_IMAGE_DESCRIPTION = os.environ.get("SECRET_KEY_IMAGE_DESCRIPTION")

if not SECRET_KEY:
    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", 'True').lower() in ['true', 'yes', '1']


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Current DJANGO_ENVIRONMENT
ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="local")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.dashboards",
    "apps.layouts",
    "apps.pages",
    "apps.authentication",
    "apps.cards",
    "apps.ui",
    "apps.extended_ui",
    "apps.icons",
    "apps.forms",
    "apps.form_layouts",
    "apps.tables",
    "apps.landing",
    "apps.gestion_produits",
    "apps.events",
    "apps.paiement",
    "apps.ModuleReclamationReponse.reclamations"
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.my_setting",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Use 'mysql' for mysqlclient or 'django.db.backends.mysql' for PyMySQL
        'NAME': 'heyyaMarket',  # Replace with your database name
        'USER': 'root',           # Replace with your MySQL username
        'PASSWORD': '',      # Replace with your MySQL password
        'HOST': 'localhost',                    # Set to your MySQL server host (e.g., 'localhost' or '127.0.0.1')
        'PORT': '3306',                         # Default MySQL port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]

# Default URL on which Django application runs for specific environment
BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # stocker les sessions en base de données
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Template Settings
# ------------------------------------------------------------------------------

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
THEME_VARIABLES = THEME_VARIABLES

AUTH_USER_MODEL = 'authentication.User'

#stripe
STRIPE_PUBLIC_KEY = 'pk_test_51Q9AeFJ8wvBEc7MTo5uzCOgnu9fOZ7CBtsFfSYbZnX6E9cC17MmlTyZsqHxhAAQaaqgccHxIfdmDBlXctnVO2XtV00AQMqxFzM'
STRIPE_SECRET_KEY = 'sk_test_51Q9AeFJ8wvBEc7MT1ORBG9uGTkKJykHOYDUaKOeK6LVIgB9PcHEJg8a1isBEDUBQgKcjOSHUldR6ira5JEdgd0Sj006TFg5Dq0'


# Email settings for Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tektaitektai7@gmail.com'  # Replace with your Gmail address
EMAIL_HOST_PASSWORD = 'jiva rlyt bqba ozzb'  # Replace with your Gmail password



# Your stuff...
# ------------------------------------------------------------------------------

# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Make sure this directory exists
TIME_ZONE = 'UTC'  # or your desired timezone
USE_TZ = True  # Make sure this is set to True



# Email settings for Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tektaitektai7@gmail.com'  # Replace with your Gmail address
EMAIL_HOST_PASSWORD = 'jiva rlyt bqba ozzb'  # Replace with your Gmail password
