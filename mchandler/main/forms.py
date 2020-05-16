from django import forms
from .models import Server  


class ServerForm(forms.ModelForm):
    error_css_class = ""
    class Meta():
        model = Server
        fields = [
            "name",
            "port",
            "version",
            "description",
            "image",
            "public",
        ]
