from django.contrib import admin
from social_django.models import Association, Nonce, UserSocialAuth

from .models import Profile

admin.site.register(Profile)
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
