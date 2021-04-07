from django.conf import settings


def providers_settings(request):
    return {
        'ACCOUNTS_PROVIDERS': settings.ACCOUNTS_PROVIDERS,
    }
