from django.contrib.auth.models import User
from django.db import models


class ServerShare(models.Model):
    """Model definition for ServerShare."""

    server = models.ForeignKey(
        to='Server',
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        verbose_name='Utilisateur',
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    manage = models.BooleanField(
        verbose_name='Démarrer / Eteindre / Paramètres de base',
        default=True,
    )
    properties = models.BooleanField(
        verbose_name='Modifier les propriétés du serveur',
        default=False,
    )
    administrators = models.BooleanField(
        verbose_name='Modifier les partages du serveur',
        default=False,
    )
    console = models.BooleanField(
        verbose_name='Accès à la console',
        default=False,
    )
