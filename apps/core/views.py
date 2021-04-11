from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ServerForm, PropertiesForm, PermissionForm
from .models import Server
from .exceptions import AlreadyRunningError, NotRunningError
from django.utils.decorators import method_decorator


# Decorators
def owner_expected(function):
    def decorator(*args, **kwargs):
        server = get_object_or_404(Server, pk=kwargs['id'])
        if server.owner != args[0].user:
            raise PermissionDenied
        return function(*args, **kwargs)
    return decorator


# Views
class Index(TemplateView):
    template_name = "core/index.html"


class PublicServersView(TemplateView):
    template_name = 'core/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['servers'] = Server.objects.filter(public=True)
        return context


@method_decorator(login_required, name='dispatch')
class ManageView(TemplateView):
    template_name = 'core/manage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['servers'] = Server.objects.filter(owner=self.request.user)
        return context


@login_required
def add(request):
    form = ServerForm(
        data=request.POST or None,
        files=request.FILES or None,
        label_suffix='',
    )

    if request.method == 'POST' and form.is_valid:
        new_server = form.save()
        new_server.owner = request.user
        new_server.save()
        messages.add_message(
            request=request,
            level=messages.INFO,
            message='Le serveur a bien été créé.',
        )
        return HttpResponseRedirect(reverse('core:edit', args=[new_server.pk]) + "?create=1")

    context = {
        'form': form,
    }
    return render(request, 'core/add.html', context)


@login_required
@owner_expected
def edit(request, id):
    server = get_object_or_404(Server, pk=id)
    form = ServerForm(
        data=request.POST or None,
        files=request.FILES or None,
        label_suffix='',
        instance=server,
    )
    if request.method == 'POST' and form.has_changed() and form.is_valid():
        form.save()
        messages.add_message(
            request=request,
            level=messages.INFO,
            message='Les paramètres du serveur on bien été enregistrés.',
        )

    context = {
        'server': server,
        'form': form,
    }
    return render(request, 'core/settings/edit.html', context)


@login_required
@owner_expected
def properties(request, id):
    server = get_object_or_404(Server, pk=id)
    properties = server.get_properties()
    form = PropertiesForm(
        data=request.POST or properties or None,
        label_suffix='',
    )
    if request.method == 'POST' and form.has_changed() and form.is_valid():
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

    context = {
        'server': server,
        'properties': properties,
        'form': form,
    }
    return render(request, 'core/settings/properties.html', context)


@login_required
@owner_expected
def permissions(request, id):
    server = get_object_or_404(Server, pk=id)
    form = PermissionForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
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
    context = {
        'server': server,
        'form': form,
        'ops': server.get_ops(),
    }
    return render(request, 'core/settings/permissions.html', context)


@login_required
@owner_expected
def delete(request, id):
    server = get_object_or_404(Server, pk=id)
    server.delete()
    messages.add_message(
        request=request,
        level=messages.INFO,
        message='Le serveur vient d\'être supprimé.',
    )
    return HttpResponseRedirect(reverse('core:manage') + "?delete=1")


@login_required
@owner_expected
def start(request, id):
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


@login_required
@owner_expected
def stop(request, id):
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
