from django.db import models
from django.contrib.auth.models import User


version_availables = [
    ('1.15.0', '1.15.0'),
    ('1.15.1', '1.15.1'),
    ('1.15.2', '1.15.2'),
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
