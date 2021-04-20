
from core.exceptions import NotRunningError
from core.forms import PropertiesForm
from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View

from core.decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization('properties'), name='dispatch')
class ServerPropertiesView(View):
    """This is the properties view."""

    def get(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        properties = server.get_properties()
        form = PropertiesForm(
            data=request.POST or properties,
            label_suffix='',
        )
        context = {
            'server': server,
            'form': form,
            'properties_created': properties is not None,
        }
        return render(request, 'core/settings/properties.html', context)

    def post(self, request, id: int):
        server = get_object_or_404(Server, pk=id)
        form = PropertiesForm(data=request.POST)
        if form.is_valid():
            server.set_properties(form.cleaned_data)
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Les propriétés du serveur on bien été enregistrées.',
            )
            if server.get_status() == 1:
                messages.add_message(
                    request=request,
                    level=messages.WARNING,
                    message='Vous devez redémarrer le serveur pour les prendre en compte.',
                )
            return HttpResponseRedirect(reverse('core:properties', args=[id]))
        else:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
            return self.get(request, id)
