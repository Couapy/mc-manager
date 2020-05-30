from django import forms
from .models import Server, ServerProperties

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit, HTML
from crispy_forms.bootstrap import FormActions


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


class PropertiesForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column(
                "gamemode",
                "difficulty",
                "view_distance",
            ),
            Column(
                "max_players",
                "level_name",
                "level_seed",
            ),
        ),
        Row(
            Column(
                "motd",
            ),
            Column(
                "spawn_protection",
                "hardcore",
                "pvp",
                "generate_structures",
            ),
        ),
        Row(
            Column(
                "spawn_npcs",
                "spawn_animals",
                "spawn_monsters",
            ),
            Column(
                "enforce_whitelist",
                "online_mode",
                "enable_command_block",
            ),
        ),
        FormActions(
            Submit('save', 'Enregistrer'),
            HTML('<input type="reset" name="cancel" value="Annuler" class="btn btn-secondary">'),
        )
    )

    class Meta:
        model = ServerProperties
        fields = [
            "max_players",
            "view_distance",
            "level_seed",
            "gamemode",
            "difficulty",
            "level_name",
            "motd",
            "spawn_protection",
            "hardcore",
            "pvp",
            "generate_structures",
            "spawn_npcs",
            "spawn_animals",
            "spawn_monsters",
            "enforce_whitelist",
            "online_mode",
            "enable_command_block",
        ]
        widgets = {
            'motd': forms.Textarea(attrs={'rows': 6})
        }
