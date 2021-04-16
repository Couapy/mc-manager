from functools import update_wrapper

from core.models import Server, ServerShare
from django.http.response import HttpResponseForbidden, HttpResponseNotFound


class CheckServerAuthorization:
    """Check user authorization."""

    def __init__(self, *args, **kwargs):
        self.func = None
        self.controls = kwargs

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
        """
        request = args[0]
        server_id = kwargs['id']
        try:
            server = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            return HttpResponseNotFound()
        if server.owner.pk != request.user.pk:
            try:
                share = ServerShare.objects.get(user=request.user)
            except ServerShare.DoesNotExist:
                return HttpResponseForbidden()
            if len(self.controls) == 0:
                return HttpResponseForbidden()
            for key in self.controls.keys():
                if getattr(share, key) != self.controls[key]:
                    return HttpResponseForbidden()
        return self.func(*args, **kwargs)
    