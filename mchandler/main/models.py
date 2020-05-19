import os

from django.contrib.auth.models import User
from django.db import models


version_availables = [
    ('1.15.0', '1.15.0'),
    ('1.15.1', '1.15.1'),
    ('1.15.2', '1.15.2'),
]

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
        max_length=6,
        choices=version_availables,
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
            return True
        else:
            return False

    def set_port_available(self):
        for port in ports_availables:
            listen = os.popen("netstat -ltunp | grep 25563").read()
            if len(listen) == 0:
                # Mettre le port dans server.conf
                command = f'cat /opt/minecraft/{self.pk}/server.conf | egrep - v "^(PORT=)"'
                conf = os.popen(command).read()
                conf += "\nPORT=" + str(port)
                with open(f"/opt/minecraft/{self.pk}/server.conf", "w+") as file:
                    file.write(conf)
                return True
        return False

    def start(self):
        """Start the service."""
        self.set_port_available()
        command = 'systemctl start minecraft@' + str(self.pk)
        # os.popen(command).read()

    def stop(self):
        """Stop the service."""
        command = 'systemctl stop minecraft@' + str(self.pk)
        os.popen(command).read()

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            # New object
            # create dir
            os.mkdir(f"/opt/minecraft/{self.pk}/")
            # copy server
            os.system(f"cp -f /opt/minecraft/servers/{self.version}.jar /opt/minecraft/{self.pk}/minecraft_server.jar")
            # set eula
            os.system(f"echo eula=true > /opt/minecraft/{self.pk}/eula.txt")
            # change permissions
            os.system(f"chown minecraft:minecraft -R /opt/minecraft/{self.pk}")
        else:
            # Update object
            pass

    def delete(self, *args, **kwargs):
        self.stop()
        os.system(f"rm -rf /opt/minecraft/{self.pk}")
        super().delete(*args, **kwargs)
