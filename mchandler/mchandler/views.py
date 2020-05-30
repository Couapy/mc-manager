from django.shortcuts import render


def index(request):
    """Index view for the site"""
    return render(request, 'index.html', {})
