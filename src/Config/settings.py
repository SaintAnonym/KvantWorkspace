"""
Django settings for KvantWorkspace project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from secret import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.43','dzhd.eivc.ru' , '127.0.0.1']


# Application definition

# Список активных приложений. Каждый элемент - имена модулей этих приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'CoreApp.apps.CoreAppConfig',
    'ChatApp.apps.ChatAppConfig',
    'NewsApp.apps.NewsAppConfig',
    'MailApp.apps.MailAppConfig',
    'AdminApp.apps.AdminAppConfig',
    'DiaryApp.apps.DiaryAppConfig',
    'LoginApp.apps.LoginAppConfig',
    'JournalApp.apps.JournalAppConfig',
    'ProjectApp.apps.ProjectAppConfig',
    'ProfileApp.apps.ProfileAppConfig',    
    'RegisterApp.apps.RegisterAppConfig',
    'NotificationApp.apps.NotificationAppConfig',

    'django_cleanup', 'storages', 'channels',
]

# MiddleWare - плагин, обрабатывающий запросы и ответы
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Определение используемого корневого модуля
ROOT_URLCONF = 'Config.urls'

# Шаблоны
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

WSGI_APPLICATION = 'Config.wsgi.application'
ASGI_APPLICATION = 'Config.asgi.application'

# Канал
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'LoginApp.KvantUser'  # Переопределение модели авторизации
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'  # Переопределение сообщенией


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# Прост доп.настроечки
# Язык веб-приложения
LANGUAGE_CODE = 'ru'

# Часовой веб-приложения
TIME_ZONE = 'Europe/Moscow'

# Необходимо для корректной работы параметра LANGUAGE_CODE
USE_I18N = True

# Будет ли локализованное форматирование. Используется формат текущей локалич
USE_L10N = True

# Использоваие временных интервалов с учетом часового пояса
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


# Setup медиа и статик файлов
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

# AWS S3 Setup
AWS_STORAGE_BUCKET_NAME = 'kvant-journal'  # Имя бакета

AWS_S3_FILE_OVERWRITE = False  # Запретить перезапись файла

# Костыль для адекватного подгруза из админ панели
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "eu-west-2"

# Setup для django-storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# S3 default image location
NEWS_DEFAULT_IMAGE = '/default/news.jpeg'
USER_DEFAULT_IMAGE = '/default/user.png'
PROJECT_DEFAULT_IMAGE = '/default/project.jpg'
USER_BANNER_DEFAULT_IMAGE = '/default/banner.jpg'
DEFAULT_AUTO_FIELD='django.db.models.AutoField' #позволяет запустить миграцию, по возможности не трогать