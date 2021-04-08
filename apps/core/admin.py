from django.contrib import admin
from .models import Server, ServerProperties


# Register your models here.
admin.site.register(Server)
admin.site.register(ServerProperties)
