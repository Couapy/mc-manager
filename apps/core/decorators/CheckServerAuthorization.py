from functools import update_wrapper

from core.models import Server, ServerShare
from django.http.response import HttpResponseForbidden, HttpResponseNotFound


class CheckServerAuthorization:
    """Check user authorization."""

    def __init__(self, *args, **kwargs):
        self.func = None
        self.controls = args

    def __call__(self, *args, **kwargs):
        """Give the function wrapper."""
        self.func = args[0]
        update_wrapper(self, self.func)
        return self.wrapper
    
    def wrapper(self, *args, **kwargs):
        """
        Verifies that the request is legitimate.
        
        Execute the route if the request user is the server owner,
        or the server owner shares the server with him.

        If the user isn't allowed to access the route, an HTTP 403 error is
        throwed.
        """
        request = args[0]
        server_id = kwargs['id']
        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            return HttpResponseNotFound()
        
        if server.is_authorized(
            user=request.user,
            controls=self.controls
        ):
            return self.func(*args, **kwargs)
        else:
            return HttpResponseForbidden()
