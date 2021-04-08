import os
import sys

import mcdwld
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Download minecraft server files to the project.ùù'

    def handle(self, *args, **options):
        """Download all servers."""
        versions = mcdwld.get_versions(
            mcdwld.MOJANG_MANIFEST_URL,
            settings.MINECRAFT_SERVERS_TYPES,
        )
        self.stdout.write(self.style.WARNING(
            'Downloading %d versions in progress, it can take a while...' % len(versions)))
        mcdwld.download_versions(
            versions,
            settings.MINECRAFT_ROOT
        )
        self.stdout.write(self.style.SUCCESS(
            'Successfully downloaded servers.'))
