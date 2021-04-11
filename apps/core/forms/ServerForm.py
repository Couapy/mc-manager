from core.models import Server
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.conf import settings


class ServerForm(forms.ModelForm):
    
    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column(
                "name",
                "public",
            ),
            Column("version"),
        ),
        "description",
        "image",
        FormActions(
            Submit('save', 'Enregistrer'),
            HTML('<input type="reset" name="cancel" value="Annuler" class="btn btn-secondary">'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        versions_installed = settings.MINECRAFT_SERVERS_LOCAL
        version_choices = []
        for version in versions_installed:
            version_choices.append((version, version))
        
        self.fields['version'] = forms.ChoiceField(
            choices=version_choices,
            label="version"
        )

    class Meta:
        model = Server
        fields = [
            "name",
            "version",
            "description",
            "image",
            "public",
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6})
        }
