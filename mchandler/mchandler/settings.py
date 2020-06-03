import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(BASE_DIR + "/config.cfg")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("DJANGO", "SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get("EMAIL", "EMAIL_HOST")
EMAIL_PORT = config.get("EMAIL", "EMAIL_PORT")
EMAIL_HOST_USER = config.get("EMAIL", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("EMAIL", "EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config.get("EMAIL", "EMAIL_USE_TLS")
EMAIL_USE_TLS = config.get("EMAIL", "EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = config.get("EMAIL", "DEFAULT_FROM_EMAIL")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Dependencies
    'social_django',
    'crispy_forms',
    'accounts',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'mchandler.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            (os.path.join(BASE_DIR, 'mchandler/templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mchandler.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'mchandler/static/')


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mchandler/media/')


# Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# OAuth authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get("GOOGLE", "KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get("GOOGLE", "SECRET")
SOCIAL_AUTH_GITHUB_KEY = config.get("GITHUB", "KEY")
SOCIAL_AUTH_GITHUB_SECRET = config.get("GITHUB", "SECRET")
SOCIAL_AUTH_TWITTER_KEY = config.get("TWITTER", "KEY")
SOCIAL_AUTH_TWITTER_SECRET = config.get("TWITTER", "SECRET")
SOCIAL_AUTH_FACEBOOK_KEY = config.get("FACEBOOK", "KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = config.get("FACEBOOK", "SECRET")

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

LOGIN_REDIRECT_URL = "/manage/"
SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTH_PROFILE_MODULE = 'accounts.Profile'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/manage/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/accounts/profile/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'

# Minecraft default configuration
MCMINMEM = config.get("MINECRAFT", "MCMINMEM")
MCMAXMEM = config.get("MINECRAFT", "MCMAXMEM")
