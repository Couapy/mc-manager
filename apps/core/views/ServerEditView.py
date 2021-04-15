
from core.exceptions import NotRunningError
from core.forms import ServerForm
from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import owner_expected


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_expected, name='dispatch')
class ServerEditView(View):
    """This is the server edit view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = ServerForm(
            data=None,
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
            label_suffix='',
            instance=server,
        )
        if form.has_changed() and form.is_valid():
            form.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Les paramètres du serveur on bien été enregistrés.',
            )
        elif form.has_changed():
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
        return HttpResponseRedirect(reverse('core:edit', args=[id]))
