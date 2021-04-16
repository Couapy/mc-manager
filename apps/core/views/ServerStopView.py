from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization(manage=True), name='dispatch')
class ServerStopView(View):
    """This is the stop view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        try:
            server.stop()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Le serveur va s\'arrêter.',
            )
        except NotRunningError:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le serveur est déjà à l\'arrêt.',
            )
        return HttpResponseRedirect(reverse('core:manage'))
