from .CheckServerAuthorization import CheckServerAuthorization
# from .CheckShareAuthorization import CheckShareAuthorization

from core.models import Server
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


def owner_expected(function):
    """Avoid users to access unauthorized data."""
    def decorator(*args, **kwargs):
        server = get_object_or_404(Server, pk=kwargs['id'])
        if server.owner != args[0].user:
            raise PermissionDenied
        return function(*args, **kwargs)
    return decorator
