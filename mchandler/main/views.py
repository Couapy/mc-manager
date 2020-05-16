from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, render,
                              reverse)

from .forms import ServerForm
from .models import Server


# Create your views here.
def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def public_servers(request):
    context = {}
    return render(request, 'main/index.html', context)


@login_required
def manage(request):
    servers = Server.objects.filter(owner=request.user)
    context = {
        'servers': servers,
        'delete_success': 'delete' in request.GET,
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
        return HttpResponseRedirect(reverse('edit', args=[new_server.pk]) + "?create=1")

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
    if request.method == 'POST' and form.is_valid:
        form.save()
        success = True

    context = {
        'server': server,
        'form': form,
        'success': success,
        'create_success': 'create' in request.GET,
    }
    return render(request, 'main/edit.html', context)


@login_required
def delete(request, id):
    server = get_object_or_404(Server, pk=id)
    server.delete()
    return HttpResponseRedirect(reverse('manage') + "?delete=1")
