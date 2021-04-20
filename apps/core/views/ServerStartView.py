from core.exceptions import AlreadyRunningError
from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views import View

from core.decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization('manage'), name='dispatch')
class ServerStartView(View):
    """This is the start view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        try:
            server.start()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Le serveur est en train de démarrer',
            )
        except AlreadyRunningError:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le serveur est déjà allumé.',
            )
        return HttpResponseRedirect(reverse('core:manage'))
