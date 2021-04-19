import json
import os
from socket import AF_UNIX, SOCK_DGRAM, socket

from core.exceptions import AlreadyRunningError, NotRunningError
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from PIL import Image

from .functions import image_upload_to
from .MinecraftInstance import SOCKFILE_NAME, MinecraftInstance
from .ServerShare import ServerShare


class Server(models.Model):
    """Minecraft server model."""

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
        upload_to=image_upload_to,
        blank=True,
        null=True,
    )

    @property
    def shares(self):
        """Give all server shares."""
        return ServerShare.objects.filter(server=self)

    def is_authorized(self, user, controls=[]):
        """
        Check if the user can access to this instance of server.

        Please see to the ServerShare model.
        """
        if len(controls) == 0:
            return False
        if self.owner.pk != user.pk:
            try:
                share = ServerShare.objects.get(user=user)
            except self.DoesNotExist:
                return False
            for control in controls:
                if not getattr(share, control):
                    return False
        return True

    def _send_command(self, command=''):
        """Send a command to the server instance."""
        if self.get_status() == 0:
            raise NotRunningError
        directory = settings.MINECRAFT_DATA_ROOT % self.pk
        sockfile = os.path.join(directory, SOCKFILE_NAME)
        sock = socket(AF_UNIX, SOCK_DGRAM)
        sock.connect(sockfile)
        sock.send(command.encode('utf-8'))
        sock.close()

    def save(self, *args, **kwargs):
        """
        Save the server properties.

        It also copy new image to server sources as server-icon.
        The image may be converted to PNG.
        """
        super().save(*args, **kwargs)

        if self.image:
            image = Image.open(self.image.path)
            width, height = image.width, image.height
            if (width > 64 or height > 64):
                filepath = os.path.join(
                    settings.MINECRAFT_DATA_ROOT % self.pk,
                    'server-icon.png'
                )
                image.thumbnail((64, 64))
                image.save(filepath, 'PNG')
    
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
        """Get administrators."""
        instance = MinecraftInstance(id=self.pk, version=self.version)
        filename = os.path.join(instance.directory, 'ops.json')
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return json.loads(content)
        except Exception:
            return []

    def get_properties(self):
        """Give server properties."""
        instance = MinecraftInstance(id=self.pk, version=self.version)
        filename = os.path.join(instance.directory, 'server.properties')
        properties = {}
        try:
            with open(filename, 'r') as file:
                lines = file.read().split('\n')
                for line in lines:
                    if line.startswith('#'):
                        continue
                    try:
                        key, value = line.split('=')
                        key = key.replace('-', '_')
                        properties[key] = value
                    except ValueError:
                        pass
        except Exception:
            return None
        return properties

    def set_properties(self, data):
        """Update server properties."""
        instance = MinecraftInstance(id=self.pk, version=self.version)
        filename = os.path.join(instance.directory, 'server.properties')
        properties = ''
        data_keys = data.keys()
        try:
            with open(filename, 'r') as file:
                lines = file.read().split('\n')
                for line in lines:
                    if line.startswith('#'):
                        properties += line + '\n'
                        continue
                    try:
                        key, value = line.split('=')
                        key_adapted = key.replace('-', '_')
                        if key_adapted in data_keys:
                            properties += '%s=%s\n' % (key, data[key_adapted])
                        else:
                            properties += line + '\n'
                    except ValueError:
                        properties += line + '\n'
        except Exception:
            pass
        properties = properties[:-1]
        with open(filename, 'w') as file:
            file.write(properties)

    def op(self, nickname):
        """Make administrator a player."""
        self._send_command('command:op %s' % nickname)

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
        self._send_command('action:close')

    def delete(self, *args, **kwargs):
        """Delete server and his data."""
        instance = MinecraftInstance(
            id=self.pk,
            version=self.version,
        )
        instance.delete_data()
        super().delete(*args, **kwargs)
