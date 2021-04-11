from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms


class PermissionForm(forms.Form):
    nickname = forms.CharField(
        max_length=128,
        label="Nom du joueur",
    )
    helper = FormHelper()
    helper.layout = Layout(
        'nickname',
        FormActions(
            Submit('save', 'Enregistrer'),
            HTML('<input type="reset" name="cancel" value="Annuler" class="btn btn-secondary">'),
        ),
    )
