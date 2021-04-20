from core.decorators import CheckServerAuthorization
from core.forms import ServerShareEditForm
from core.models import Server, ServerShare
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
@method_decorator(CheckServerAuthorization('administrators'), name='dispatch')
class ServerShareEditView(View):
    """This is the share edit view."""

    def get(self, request, id: int, share_id: int):
        share = get_object_or_404(ServerShare, pk=share_id)
        form = ServerShareEditForm(
            data=request.POST or None,
            instance=share,
        )
        context = {
            'server': share.server,
            'share': share,
            'user_share': share.user,
            'form': form,
        }
        return render(request, 'core/settings/share_edit.html', context)

    def post(self, request, id: int, share_id: int):
        share = get_object_or_404(ServerShare, pk=share_id)
        form = ServerShareEditForm(
            data=request.POST,
            instance=share,
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request=request,
                level=messages.INFO,
                message='Le partage a bien été modifié.',
            )
            return HttpResponseRedirect(reverse('core:shares', args=[id]))
        else:
            messages.add_message(
                request=request,
                level=messages.ERROR,
                message='Le formulaire est incorrect.',
            )
        return self.get(request, id, share_id)
