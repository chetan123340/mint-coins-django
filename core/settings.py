"settings file - here we have all the constants and configurations"
import os
from pathlib import Path


import firebase_admin
from firebase_admin import credentials




# Download the service account key from Firebase Console and place it in your project
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, options = {
    "databaseURL":"https://mint-coins-default-rtdb.firebaseio.com"
})

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "lr9b%=-zx)mn!)fw%n847+^tp@4k-2lh+py+66cn$7kzi9s!zi"

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://extremely-rested-fowl.ngrok-free.app"
]

# SET difficulty - difficulty defines how many zeroes should it contain in prefix
MINING_DIFFICULTY = 3
# How much reward should be given for mining
MINING_REWARD = 50

STARTING_AMOUNT = 1000

INSTALLED_APPS = [
    'main',
    'qr_code',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
LOGIN_REDIRECT_URL = "account"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = 'main.LillyUser'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'