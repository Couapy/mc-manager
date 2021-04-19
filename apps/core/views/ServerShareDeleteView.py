from core.models import ServerShare
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views import View

from core.decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization('administrators'), name='dispatch')
class ServerShareDeleteView(View):
    """This is the server share delete view."""

    def get(self, request, id: int, share_id: int):
        share = get_object_or_404(ServerShare, pk=share_id)
        share.delete()
        messages.add_message(
            request=request,
            level=messages.INFO,
            message='Le partage vient d\'être supprimé.',
        )
        return HttpResponseRedirect(reverse('core:shares', args=[share.server.pk]))
