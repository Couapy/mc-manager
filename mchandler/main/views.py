from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)

from .forms import ServerForm, PropertiesForm, PermissionForm
from .models import Server, ServerProperties


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def public_servers(request):
    context = {
        'servers': Server.objects.filter(public=True)
    }
    return render(request, 'main/list.html', context)


@login_required
def manage(request):
    servers = Server.objects.filter(owner=request.user)
    context = {
        'servers': servers,
        'delete_success': 'delete' in request.GET,
        'start_success': 'start' in request.GET,
        'stop_success': 'stop' in request.GET,
    }
    return render(request, 'main/manage.html', context)


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
        return HttpResponseRedirect(reverse('main:edit', args=[new_server.pk]) + "?create=1")

    context = {
        'form': form,
    }
    return render(request, 'main/add.html', context)


@login_required
def edit(request, id):
    server = get_object_or_404(Server, pk=id)
    form = ServerForm(
        data=request.POST or None,
        files=request.FILES or None,
        label_suffix='',
        instance=server,
    )
    success = None
    if request.method == 'POST':
        if form.has_changed() and form.is_valid():
            form.save()
            success = True

    context = {
        'server': server,
        'form': form,
        'success': success,
        'create_success': 'create' in request.GET,
    }
    return render(request, 'main/settings/edit.html', context)


@login_required
def properties(request, id):
    server = get_object_or_404(Server, pk=id)
    properties = get_object_or_404(ServerProperties, server=server)
    form = PropertiesForm(
        data=request.POST or None,
        label_suffix='',
        instance=properties,
    )
    success = None
    if request.method == 'POST':
        if form.has_changed() and form.is_valid():
            form.save()
            success = True

    context = {
        'server': server,
        'properties': properties,
        'form': form,
        'success': success,
    }
    return render(request, 'main/settings/properties.html', context)


@login_required
def permissions(request, id):
    server = get_object_or_404(Server, pk=id)
    form = PermissionForm(
        data=request.POST or None,
    )
    success = None
    if request.method == 'POST':
        if form.is_valid():
            server.op(form.cleaned_data['nickname'])
            success = True
    ops = server.get_ops()

    context = {
        'server': server,
        'form': form,
        'success': success,
        'ops': ops,
    }
    return render(request, 'main/settings/permissions.html', context)


@login_required
def delete(request, id):
    server = get_object_or_404(Server, pk=id)
    server.delete()
    return HttpResponseRedirect(reverse('main:manage') + "?delete=1")


@login_required
def start(request, id):
    server = get_object_or_404(Server, pk=id)
    if server.owner == request.user:
        server.start()
    return HttpResponseRedirect(reverse('main:manage') + "?start=1")


@login_required
def stop(request, id):
    server = get_object_or_404(Server, pk=id)
    if server.owner == request.user:
        server.stop()
    return HttpResponseRedirect(reverse('main:manage') + "?stop=1")
