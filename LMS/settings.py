"""
Django settings for LMS project.
"""

from pathlib import Path

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY
# ==========================================

SECRET_KEY = 'django-insecure-n++lpd-2cgiontz+rg9y4mi=qv2p7_tu@i3emb!5d48h%+i1nv'

DEBUG = True

ALLOWED_HOSTS = []


# ==========================================
# INSTALLED APPS
# ==========================================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # PROJECT APPS

    'accounts',
    'student',
    'teacher',
    'librarian',
    'books',
    'fines',
    'issue',

    # THIRD PARTY APPS

    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]


# ==========================================
# REST FRAMEWORK
# ==========================================

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

    'DEFAULT_PERMISSION_CLASSES': (

        'rest_framework.permissions.AllowAny',

    )
}


# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================
# URL CONFIGURATION
# ==========================================

ROOT_URLCONF = 'LMS.urls'


# ==========================================
# TEMPLATES
# ==========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================
# WSGI
# ==========================================

WSGI_APPLICATION = 'LMS.wsgi.application'


# ==========================================
# DATABASE
# ==========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# PASSWORD VALIDATION
# ==========================================

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


# ==========================================
# INTERNATIONALIZATION
# ==========================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# ==========================================
# MEDIA FILES
# ==========================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# LOGIN SETTINGS
# ==========================================

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/librarian/dashboard/'


# ==========================================
# SESSION SETTINGS
# ==========================================

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ==========================================
# CORS
# ==========================================

CORS_ALLOW_ALL_ORIGINS = True


# ==========================================
# CUSTOM USER MODEL
# ==========================================

AUTH_USER_MODEL = 'accounts.CustomUser'

CSRF_FAILURE_VIEW = 'accounts.views.csrf_error'
# ==========================================
# DEFAULT PRIMARY KEY
# ==========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'