from os.path import join

from django.conf import settings


def image_upload_to(instance, filename: str):
    """Give the file path for uploading server icon."""
    filepath = join(
        'server',
        'server-icon_%.3d.png',
    )
    return filepath % instance.pk
