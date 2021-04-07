from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


def user_directory_path(instance, filename):
    """
    Indicates the location for saving a profile picture.

    Files will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    """
    return 'avatar/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    """Reprsents a user profile."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="related user",
    )
    biography = models.TextField(
        verbose_name="biography",
        help_text="300 characters maximum",
        max_length=300,
        blank=True,
        null=True,
    )
    website = models.URLField(
        verbose_name="web site",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        verbose_name="profil picture",
        upload_to=user_directory_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.__str__()
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile and assign it to every new user."""
    if created:
        Profile.objects.create(user=instance)
