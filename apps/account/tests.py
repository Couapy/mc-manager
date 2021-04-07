from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile


class ProfileTestCase(TestCase):
    """Tests for profile model."""

    def test_auto_create_profile(self):
        """Automatically create profile for new users."""
        user = User.objects.create(username="user_new_profile")
        profile = Profile.objects.last()
        self.assertNotEqual(user.profile, None)
        self.assertEqual(user.profile, profile)
