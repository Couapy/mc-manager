import json
import os
from uuid import uuid1

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_versions_availables():
    try:
        servers = os.listdir('/opt/minecraft/servers/')
    except Exception:
        servers = []
    versions = []
    for server in servers:
        (filename, ext) = os.path.splitext(server)
        versions.append((server, filename))
    return versions


versions_availables = get_versions_availables()
ports_availables = [
    25565,
    25564,
    25563,
]
share_level_choices = [
    ("full", "Démarrage, configuration et repartage"),
    ("standard", "Démarrage et configuration"),
    ("strict", "Démarrage uniquement"),
]


class ServerShare(models.Model):
    user = models.ForeignKey(
        verbose_name="Utilisateur",
        to=User,
        on_delete=models.CASCADE
    )
    level = models.CharField(
        verbose_name="Type de permission",
        max_length=8,
        choices=share_level_choices,
    )


class Server(models.Model):
    """This is the model for a server."""

    name = models.CharField(
        verbose_name="Nom",
        max_length=64,
    )
    public = models.BooleanField(
        verbose_name="Serveur public",
        default=False,
    )
    port = models.IntegerField(
        verbose_name="Port",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=100,
        default="A minecraft server"
    )
    version = models.CharField(
        verbose_name="Version",
        max_length=32,
        choices=versions_availables,
    )
    image = models.ImageField(
        verbose_name="Icone",
        blank=True,
        null=True,
    )
    shares = models.ManyToManyField(


        ServerShare,
    )

    def get_image(self):
        """Return the image url"""
        if bool(self.image):
            return self.image.url
        else:
            return False

    def get_status(self):
        command = 'systemctl status minecraft@' + str(self.pk)
        res = os.popen(command).read()
        if res.find('Active: active') != -1:
            return 2
        elif res.find('Active: activating') != -1:
            return 1
        else:
            return 0

    def op(self, nickname):
        """Op a player."""
        if self.get_status() == 2:
            command = f"sudo -u minecraft /usr/bin/screen -p 0 -S mc-{self.pk} -X eval 'stuff \"op {nickname}\"\\015'"
            os.system(command)

    def get_ops(self):
        filename = f"/opt/minecraft/{self.pk}/ops.json"
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return json.loads(content)
        except Exception:
            return []

    def start(self):
        """Start the service."""
        properties = ServerProperties.objects.get(server=self)
        properties.update()

        for port in ports_availables:
            listen = os.popen(f"netstat -ltun | grep {port}").read()
            if len(listen) == 0:
                file_path = f"/opt/minecraft/{self.pk}/server.conf"
                file_path_temp = f"/tmp/" + str(uuid1()) + ".server.conf"

                # Update the RAM and PORT configuration
                config = f"MCMINMEM={settings.MCMINMEM}\n"
                config += f"MCMAXMEM={settings.MCMAXMEM}\n"
                config += f"PORT={port}\n"
                with open(file_path_temp, 'w+') as file:
                    file.write(config)
                os.system(f"sudo -u minecraft cp -f {file_path_temp} {file_path}")
                os.system(f"rm -f {file_path_temp}")

                # Start the server
                self.port = port
                self.save()
                os.system("sudo systemctl start minecraft@" + str(self.pk) + " &")
                break

    def stop(self):
        """Stop the service."""
        os.system("sudo systemctl stop minecraft@" + str(self.pk) + " &")

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        prefix = "sudo -u minecraft "
        if new:
            os.system(prefix + f"mkdir /opt/minecraft/{self.pk}")
            os.system(prefix + f"echo \"eula=true\" > /opt/minecraft/{self.pk}/eula.txt")
        os.system(prefix + f"cp -f /opt/minecraft/servers/{self.version} /opt/minecraft/{self.pk}/minecraft_server.jar")

    def delete(self, *args, **kwargs):
        self.stop()
        os.system(f"sudo -u minecraft rm -rf /opt/minecraft/{self.pk}")
        super().delete(*args, **kwargs)


class ServerProperties(models.Model):
    """server.properties"""

    server = models.OneToOneField(
        to=Server,
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
            if name not in['id', 'server']:
                properties[name] = str(value)

        for name, property in properties.items():
            result += name + "=" + str(property) + "\n"

        properties_file_temp = "/tmp/" + str(uuid1()) + ".server.properties"
        with open(properties_file_temp, "w+") as temp_file:
            temp_file.write(result)

        command = f"cp -f {properties_file_temp} {properties_file}"
        os.system(f"sudo -u minecraft {command}")
        os.system(f"sudo rm -f {properties_file_temp}")


@receiver(post_save, sender=Server)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ServerProperties.objects.create(
            server=instance,
        )
