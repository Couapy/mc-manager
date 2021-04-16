from core.forms import ServerShareForm
from core.models import Server, ServerShare
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import CheckServerAuthorization


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization(administrators=True), name='dispatch')
class ServerSharesView(View):
    """This is the share view."""

    def get(self, request, id):
        server = get_object_or_404(Server, pk=id)
        form = ServerShareForm(data=None)
        context = {
            'server': server,
            'form': form,
        }
        return render(request, 'core/settings/shares.html', context)

    def post(self, request, id):
        server = get_object_or_404(Server, pk=id)
        form = ServerShareForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.POST['user'])
            try:
                share = ServerShare.objects.get(server=server, user=user)
            except ServerShare.DoesNotExist:
                share = None
            if share:
                form = ServerShareForm(
                    data=request.POST,
                    instance=share,
                )
                form.save()
                messages.add_message(
                    request=request,
                    level=messages.INFO,
                    message='Le partage existant a été modifié.',
                )
            else:
                share = form.save()
                share.server = server
                share.save()
                messages.add_message(
                    request=request,
                    level=messages.INFO,
                    message='Le partage a bien été créé.',
                )
            return HttpResponseRedirect(reverse('core:shares', args=[id]))
        else:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
        return self.get(request, id)
