import os

import mcdwld
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Download minecraft server files to the project.ùù'

    def handle(self, *args, **options):
        """Download all servers."""
        downloads_directory = os.getcwd() + '/downloads/'
        versions = mcdwld.get_versions(mcdwld.MOJANG_MANIFEST_URL)
        mcdwld.download_versions(versions, downloads_directory)
        self.stdout.write(self.style.SUCCESS('Successfully downloaded servers.'))
