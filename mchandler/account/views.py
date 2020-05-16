from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render


@login_required
def profile(request):
    return render(request, 'account/profile.html', {})


def login(request):
    """This is the view for login."""
    return render(request, 'account/login.html', {})


@login_required
def logout(request):
    """This is the view for logout."""
    auth.logout(request)
    return HttpResponseRedirect('/')
