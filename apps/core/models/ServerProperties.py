from django.conf import settings
from django.db import models


class ServerProperties(models.Model):
    """server.properties"""

    # TODO : déplacer vers form et hydrater depuis le fichier 
    #        server.porperties

    server = models.OneToOneField(
        to='Server',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    max_players = models.IntegerField(
        verbose_name="Maximum de joueurs",
        default=5,
    )
    view_distance = models.IntegerField(
        verbose_name="Distance de rendu (en chunck)",
        default=10,
    )
    level_seed = models.CharField(
        verbose_name="Seed du monde",
        max_length=128,
        null=True,
        blank=True,
    )
    gamemode = models.CharField(
        verbose_name="Mode de jeu",
        max_length=9,
        choices=[
            ('survival', 'Survie'),
            ('creative', 'Creatif'),
            ('spectator', 'Spectateur'),
            ('adventure', 'Aventure'),
        ],
        default='survival',
    )
    force_gamemode = models.BooleanField(
        verbose_name="Forcer le gamemode",
        default=True,
    )
    difficulty = models.CharField(
        verbose_name="Difficulté",
        max_length=8,
        choices=[
            ('peaceful', 'Paisible'),
            ('easy', 'Facile'),
            ('normal', 'Normale'),
            ('hard', 'Difficile'),
        ],
        default='normal',
    )
    level_name = models.CharField(
        verbose_name="Nom du monde",
        max_length=32,
        default='world',
    )
    motd = models.TextField(
        verbose_name="Description du serveur",
        max_length=300,
        default="A Minecraft Server"
    )
    spawn_protection = models.IntegerField(
        verbose_name="Protection du spawn (en block)",
        default=0,
    )
    hardcore = models.BooleanField(
        verbose_name="Hardcore",
        default=False,
    )
    pvp = models.BooleanField(
        verbose_name="PVP",
        default=True,
    )
    generate_structures = models.BooleanField(
        verbose_name="Générer des structures",
        default=True,
    )
    spawn_npcs = models.BooleanField(
        verbose_name="Villageois",
        default=True,
    )
    spawn_animals = models.BooleanField(
        verbose_name="Animaux",
        default=True,
    )
    spawn_monsters = models.BooleanField(
        verbose_name="Monstres",
        default=True,
    )
    enforce_whitelist = models.BooleanField(
        verbose_name="Activer la liste blanche",
        default=False,
    )
    online_mode = models.BooleanField(
        verbose_name="Autoriser seulement les comptes légaux",
        default=True,
    )
    enable_command_block = models.BooleanField(
        verbose_name="Activer les command blocks",
        default=False,
    )

    @property
    def properties(self):
        file_name = f"/opt/minecraft/{self.pk}/server.properties"
        properties = {}
        try:
            with open(file_name, 'r') as properties_file:
                content = properties_file.read()
                for ligne in content.split("\n"):
                    if not ligne.startswith("#") and "=" in ligne:
                        name, property = ligne.split("=")
                        properties[name] = property
        except Exception:
            pass
        return properties

    def update(self):
        properties_file = f"/opt/minecraft/{self.pk}/server.properties"
        properties = self.properties
        result = ''

        for field in self._meta.get_fields():
            value = self._meta.get_field(field.name).value_from_object(self)
            name = field.name.replace('_', '-')
            if name not in ['id', 'server']:
                properties[name] = str(value)

        for name, value in properties.items():
            result += name + "=" + str(value) + "\n"

        properties_file_temp = "/tmp/" + str(uuid1()) + ".server.properties"
        with open(properties_file_temp, "w+") as temp_file:
            temp_file.write(result)

        command = f"cp -f {properties_file_temp} {properties_file}"
        os.system(f"sudo -u minecraft {command}")
        os.system(f"sudo rm -f {properties_file_temp}")
