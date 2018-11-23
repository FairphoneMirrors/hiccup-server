"""
Django settings for hiccup_server project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "7u+#ha3hk!x+*)clhs46%n*)w1q+5s4+yoc#1!nm0b%fwwrud@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "crashreports",
    "crashreport_stats",
    "taggit",
    "crispy_forms",
    "bootstrap3",
    "bootstrapform",
    "django_extensions",
    "django_filters",
    "djfrontend",
    "djfrontend.skeleton",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "drf_yasg",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hiccup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "hiccup", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ]
        },
    }
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# WSGI_APPLICATION = 'hiccup_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": "",  # Connect to database through UNIX domain sockets
        "PORT": "",  # Not needed for UNIX domain sockets
        "NAME": os.environ.get("USER"),
        "USER": os.environ.get("USER"),
        "PASSWORD": "",  # Not needed for UNIX domain sockets
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator"
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "PAGE_SIZE": 100,
}

SITE_ID = 1

SOCIALACCOUNT_ADAPTER = "hiccup.allauth_adapters.FairphoneAccountAdapter"
LOGIN_REDIRECT_URL = "/hiccup_stats/"
# disable form signups
ACCOUNT_ADAPTER = "hiccup.allauth_adapters.FormAccountAdapter"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "crashreport_uploads")


# Logging
# https://docs.djangoproject.com/en/2.0/topics/logging/#examples

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
        }
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
        "hiccup": {"handlers": ["file"], "level": "DEBUG", "propagate": True},
        "crashreports": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "crashreport_stats": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Automatic documentation generation
# https://drf-yasg.readthedocs.io/en/stable/index.html

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "hiccup.urls.api_info",
    "SECURITY_DEFINITIONS": {
        "Device token authentication": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": (
                "Authenticate using a token that was returned on successful "
                "registration of a new device. The token can only be used to "
                "authenticate requests that target the device with the "
                "matching UUID. The token has to be put in the request header: "
                "'Authorization: Token <AUTH_TOKEN>'"
            ),
        },
        "Google OAuth": {
            "type": "oauth2",
            "flow": "implicit",
            "authorizationUrl": "/accounts/google/login/callback/",
            "scopes": {},
            "description": (
                "Authenticate using a Google account. Only E-mail addresses "
                "in the @fairphone.com domain are allowed."
            ),
        },
    },
}

try:
    from local_settings import *  # noqa: F403,F401 pylint: disable=W0401,W0614
except ImportError:
    pass
