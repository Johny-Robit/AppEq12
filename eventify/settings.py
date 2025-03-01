import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Sécurité
SECRET_KEY = os.getenv('SECRET_KEY')


# TODO don't run with debug turned on in production!
DEBUG = True
# Domaines autorisés
# TODO inscrire notre domaine une fois le déploiement sur Heroku

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



ALLOWED_HOSTS = [
    'app-eq-12-eventify-29bf10cbb7c2.herokuapp.com',
    'johny-robit.github.io',
    'localhost',
    '127.0.0.1',
    'http://localhost:5173',
    'http://localhost:5173/AppEq12/'
]


# CORS_ALLOWED_ORIGINS = [
#     "https://johny-robit.github.io", 
#     "http://localhost:5173",
#     "https://app-eq-12-eventify-29bf10cbb7c2.herokuapp.com"  # Ajoute ton API déployée
# ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://app-eq-12-eventify-29bf10cbb7c2.herokuapp.com",
    "https://johny-robit.github.io"
]



CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-requested-with",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# Applications Django
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Packages
    'rest_framework',

    # Application interne
    'events'
]

# Le fichier racine pour les urls
ROOT_URLCONF = 'eventify.urls'

# Authentification sur mesure avec token stocké en base
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "events.authentication.TokenAuthentication",
    ],
}

AUTH_USER_MODEL = "events.CustomUser"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Paramètrage pour la validation de passwords
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


WSGI_APPLICATION = 'eventify.wsgi.application'


# Paramètres divers
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Pour pytest-django
pytest_plugins = ["django.contrib.auth"]

# Logging
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'eventify_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'eventify.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'events_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'events.log'),
            'maxBytes': 1024 * 1024 * 5,  
            'backupCount': 3,  
            'formatter': 'verbose',
        },
        #'django_file': {  # DEBUG Nouveau handler pour Django
        #    'level': 'DEBUG',
        #    'class': 'logging.FileHandler',
        #    'filename': os.path.join(LOG_DIR, 'debug.log'),
        #    'formatter': 'verbose',
        #},
    },
    'loggers': {
        'eventify': {
            'handlers': ['console', 'eventify_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'events': {
            'handlers': ['console', 'events_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        #'django': {  # DEBUG Nouveau logger pour Django
        #    'handlers': ['console', 'django_file'],
        #    'level': 'DEBUG',
        #    'propagate': True,
        #},
    },
}





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
