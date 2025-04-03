"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import dj_database_url
from pathlib import Path
import os

import environ

from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _

# Création d'une instance d'Environnement
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture des variables d'environnement depuis le fichier .env situé à la racine du projet
environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "=n_d@%w72^mc4=700l5+-d-_&#trp)sj-%l^($#p-5uw%hjoeh")
# 'django-insecure-u500^nk*0)p&=7=r0#4g%_7zcs3cgf-vjncqvd9do%qblh)q$t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

PORT = os.environ.get("PORT", "10000")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost 127.0.0.1").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modeltranslation',
    'widget_tweaks',
    'store',
    'accounts',
    'ckeditor',
    'tailwind',
    'theme',
    'django_browser_reload'
]

# setup for tailwind
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# Whitenoise for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]



ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# PostgreSQL Database Setup
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
# postgresql://theperfectgift_postresql_user:1YccuMjb1JzyDHgcZcVb5FY10OG3z1c8@dpg-cvcnr6t6l47c73fkl6dg-a.frankfurt-postgres.render.com/theperfectgift_postresql

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('Français')),
    ('nl', _('Nederlands')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# Path for translations files
LOCALE_PATHS = [
    BASE_DIR / 'locale', 
]

# Ignore les fichiers et dossiers indésirables pendant la traduction
XGETTEXT_OPTIONS = '--keyword=gettext_noop --keyword=gettext_lazy --keyword=ngettext_lazy:1,2 --keyword=pgettext:1c,2 --keyword=npgettext:1c,2,3 --from-code=UTF-8'
# Exclure certains chemins automatiquement
GETTEXT_EXCLUDED_DIRS = ['node_modules', 'env', 'venv', '.git', '__pycache__']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/" #URL dans le navigateur
MEDIA_ROOT = "/products/" #Dossier sur le serveur
# MEDIA_ROOT = BASE_DIR / "media/" #Dossier sur le serveur local

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.Shopper"
STRIPE_API_KEY = env("STRIPE_API_KEY")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"