from core.models import ServerShare
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.conf import settings


class ServerShareForm(forms.ModelForm):
    
    helper = FormHelper()
    helper.layout = Layout(
        'user',
        'manage',
        'properties',
        'administrators',
        'console',
        FormActions(
            Submit('save', 'Enregistrer'),
            HTML('<input type="reset" name="cancel" value="Annuler" class="btn btn-secondary">'),
        )
    )

    class Meta:
        model = ServerShare
        fields = [
            'administrators',
            'console',
            'manage',
            'properties',
            'user',
        ]
