from django.contrib import admin
from .models import ServerShare, Server, ServerProperties


# Register your models here.
admin.site.register(ServerShare)
admin.site.register(Server)
admin.site.register(ServerProperties)
