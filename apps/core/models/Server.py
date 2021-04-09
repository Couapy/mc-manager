import os
from socket import AF_UNIX, SOCK_DGRAM, socket

from core.exceptions import AlreadyRunningError, NotRunningError
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .MinecraftInstance import SOCKFILE_NAME, MinecraftInstance


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
        to=User,
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
    )
    image = models.ImageField(
        verbose_name="Icone",
        blank=True,
        null=True,
    )

    def get_status(self):
        """
        Give current status of the server instance.

        There is two possible anwsers :
        * running -> 1
        * stopped -> 0
        """
        directory = settings.MINECRAFT_DATA_ROOT % self.pk
        sockfile = os.path.join(directory, SOCKFILE_NAME)
        if os.path.exists(sockfile):
            try:
                sock = socket(AF_UNIX, SOCK_DGRAM)
                sock.connect(sockfile)
                sock.close()
            except IOError:
                return 0
            return 1
        else:
            return 0

    def get_ops(self):
        filename = f"/opt/minecraft/{self.pk}/ops.json"
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return json.loads(content)
        except Exception:
            return []

    def start(self):
        """Start an instance of the server."""
        if self.get_status() == 1:
            raise AlreadyRunningError
        instance = MinecraftInstance(
            id=self.pk,
            version=self.version
        )
        instance.start()

    def stop(self):
        """Stop the service."""
        if self.get_status() == 0:
            raise NotRunningError
        directory = settings.MINECRAFT_DATA_ROOT % self.pk
        sockfile = os.path.join(directory, SOCKFILE_NAME)
        sock = socket(AF_UNIX, SOCK_DGRAM)
        sock.connect(sockfile)
        sock.send('action:close'.encode('utf-8'))
        sock.close()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        instance = MinecraftInstance(
            id=self.pk,
            version=self.version
        )
        instance.delete_data()


@receiver(post_save, sender=Server)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ServerProperties.objects.create(
            server=instance,
        )
