
from core.exceptions import NotRunningError
from core.forms import ServerForm
from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View

from core.decorators import CheckServerAuthorization, owner_expected


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization('manage'), name='dispatch')
class ServerEditView(View):
    """This is the server edit view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = ServerForm(
            data=request.POST or None,
            instance=server,
        )
        context = {
            'server': server,
            'form': form,
        }
        return render(request, 'core/settings/edit.html', context)

    def post(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = ServerForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=server,
        )
        if form.has_changed() and form.is_valid():
            form.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Les paramètres du serveur ont bien été enregistrés.',
            )
        return self.get(request, id)
