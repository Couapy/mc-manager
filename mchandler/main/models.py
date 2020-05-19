import os

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def get_version_availables():
    servers = os.listdir('/opt/minecraft/servers/')
    versions = []
    for server in servers:
        (filename, ext) = os.path.splitext(server)
        versions.append(
            (server, filename)
        )
    return versions


versions_availables = get_version_availables()
ports_availables = [
    25565,
    25564,
    25563,
]


# Create your models here.
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
        default='1.15.2',
    )
    image = models.ImageField(
        verbose_name="Icone",
        blank=True,
        null=True,
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

    def start(self):
        """Start the service."""
        for port in ports_availables:
            listen = os.popen("netstat -ltunp | grep 25563").read()
            if len(listen) == 0:
                os.system(
                    "sudo -u minecraft sh {settings.BASE_DIR}/main/scripts/config.sh "
                    + "{self.pk} 256M 4G {port}"
                )
                os.system("sudo systemctl start minecraft@" + str(self.pk))
            return

    def stop(self):
        """Stop the service."""
        command = "sudo systemctl stop minecraft@" + str(self.pk)
        os.system(command)

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            command = "sudo -u minecraft "
            command += f"sh {settings.BASE_DIR}/main/scripts/new.sh {self.pk} {self.version}"
            os.system(command)
        else:
            pass

    def delete(self, *args, **kwargs):
        self.stop()
        os.system(f"rm -rf /opt/minecraft/{self.pk}")
        super().delete(*args, **kwargs)
