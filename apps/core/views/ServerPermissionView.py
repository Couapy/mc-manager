from core.exceptions import NotRunningError
from core.forms import PermissionForm
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
class ServerPermissionView(View):
    """This is the permission view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = PermissionForm()
        context = {
            'server': server,
            'form': form,
            'ops': server.get_ops(),
        }
        return render(request, 'core/settings/permissions.html', context)

    def post(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = PermissionForm(data=request.POST or None)
        if form.is_valid():
            try:
                server.op(form.cleaned_data['nickname'])
                name = form.cleaned_data['nickname']
                message = '%s a bien été ajouté à la liste des administrateurs' % name
                messages.add_message(
                    request=request,
                    level=messages.INFO,
                    message=message,
                )
                messages.add_message(
                    request=request,
                    level=messages.WARNING,
                    message='L\'information va être traitée sous peu.' +
                    ' Vous devrez peut-être recharcher cette page pour voir apparaître un changement.'
                )
            except NotRunningError:
                messages.add_message(
                    request=request,
                    level=messages.ERROR,
                    message='Le serveur est à l\'arrêt. Impossible de traiter la demande',
                )
        else:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
        return HttpResponseRedirect(reverse('core:permissions', args=[id]))
        