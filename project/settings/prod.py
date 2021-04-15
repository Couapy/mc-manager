from project.settings.base import config

DEBUG = False

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mcmanager',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('EMAIL', 'EMAIL_HOST')
EMAIL_PORT = config.get('EMAIL', 'EMAIL_PORT')
EMAIL_HOST_USER = config.get('EMAIL', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL', 'EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config.get('EMAIL', 'EMAIL_USE_TLS')
EMAIL_USE_TLS = config.get('EMAIL', 'EMAIL_USE_SSL')
DEFAULT_FROM_EMAIL = config.get('EMAIL', 'DEFAULT_FROM_EMAIL')
