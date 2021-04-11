from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms


class PropertiesForm(forms.Form):
    """server.properties form."""

    # Fields
    max_players = forms.IntegerField(
        label="Maximum de joueurs",
    )
    view_distance = forms.IntegerField(
        label="Distance de rendu (en chunck)",
    )
    level_seed = forms.CharField(
        label="Seed du monde",
        required=False,
        max_length=128,
        # null=True,
        # blank=True,
    )
    gamemode = forms.ChoiceField(
        label="Mode de jeu",
        choices=[
            ('survival', 'Survie'),
            ('creative', 'Creatif'),
            ('spectator', 'Spectateur'),
            ('adventure', 'Aventure'),
        ],
    )
    force_gamemode = forms.BooleanField(
        label="Forcer le gamemode",
        required=False,
    )
    difficulty = forms.ChoiceField(
        label="Difficulté",
        choices=[
            ('peaceful', 'Paisible'),
            ('easy', 'Facile'),
            ('normal', 'Normale'),
            ('hard', 'Difficile'),
        ],
    )
    level_name = forms.CharField(
        label="Nom du monde",
        max_length=32,
    )
    motd = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6}),
        label="Description du serveur",
        max_length=300,
    )
    spawn_protection = forms.IntegerField(
        label="Protection du spawn (en block)",
    )
    hardcore = forms.BooleanField(
        label="Hardcore",
        required=False,
    )
    pvp = forms.BooleanField(
        label="PVP",
        required=False,
    )
    generate_structures = forms.BooleanField(
        label="Générer des structures",
        required=False,
    )
    spawn_npcs = forms.BooleanField(
        label="Villageois",
        required=False,
    )
    spawn_animals = forms.BooleanField(
        label="Animaux",
        required=False,
    )
    spawn_monsters = forms.BooleanField(
        label="Monstres",
        required=False,
    )
    white_list = forms.BooleanField(
        label="Activer la liste blanche",
        required=False,
    )
    online_mode = forms.BooleanField(
        label="Autoriser seulement les comptes légaux",
        required=False,
    )
    enable_command_block = forms.BooleanField(
        label="Activer les command blocks",
        required=False,
    )

    # Layout configuration
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
                "force_gamemode",
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
                "white_list",
                "online_mode",
                "enable_command_block",
            ),
        ),
        FormActions(
            Submit('save', 'Enregistrer'),
            HTML(
                '<input type="reset" name="cancel" value="Annuler" class="btn btn-secondary">'),
        )
    )
