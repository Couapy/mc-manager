import os
import configparser


# Constants
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Configuration
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.cfg'))


# Security
SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = []
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


# Applications
INSTALLED_APPS = [
    # Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Dependencies
    'social_django',
    'crispy_forms',
    # My applications
    'account',
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
]
ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            (os.path.join(BASE_DIR, 'project/templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.providers_settings',
            ],
        },
    },
]
WSGI_APPLICATION = 'project.wsgi.application'


# Authentication
ACCOUNTS_PROVIDERS = [
    {
        'provider': 'google-oauth2',
        'name': 'Google',
        'link': None,
        'username': None,
    },
    {
        'provider': 'github',
        'name': 'Github',
        'link': 'https://github.com/{{ data.login }}',
        'username': '{{ data.login }}',
    },
    {
        'provider': 'twitter',
        'name': 'Twitter',
        'link': 'https://twitter.com/{{ data.access_token.screen_name }}/',
        'username': '@{{ data.access_token.screen_name }}',
    },
    {
        'provider': 'facebook',
        'name': 'Facebook',
        'link': None,
        'username': None,
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get('GOOGLE', 'KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get('GOOGLE', 'SECRET')
SOCIAL_AUTH_GITHUB_KEY = config.get('GITHUB', 'KEY')
SOCIAL_AUTH_GITHUB_SECRET = config.get('GITHUB', 'SECRET')
SOCIAL_AUTH_TWITTER_KEY = config.get('TWITTER', 'KEY')
SOCIAL_AUTH_TWITTER_SECRET = config.get('TWITTER', 'SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = config.get('FACEBOOK', 'KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config.get('FACEBOOK', 'SECRET')

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/profile/'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTH_PROFILE_MODULE = 'account.Profile'

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

SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'


# Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'var/static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'var/media/')


# Locale
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
