from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization(), name='dispatch')
class ServerDeleteView(View):
    """This is the delete view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        server.delete()
        messages.add_message(
            request=request,
            level=messages.INFO,
            message='Le serveur vient d\'être supprimé.',
        )
        return HttpResponseRedirect(reverse('core:manage'))
