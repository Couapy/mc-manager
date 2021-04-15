from core.exceptions import NotRunningError
from core.forms import ServerForm
from core.models import Server
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class ServerCreateView(View):
    """This is the server create view."""

    def get(self, request):
        form = ServerForm(data=request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'core/add.html', context)

    def post(self, request):
        form = ServerForm(
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            new_server = form.save()
            new_server.owner = request.user
            new_server.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Le serveur a bien été créé.',
            )
            return HttpResponseRedirect(reverse('core:edit', args=[new_server.pk]))
        else:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
        self.get(request)
