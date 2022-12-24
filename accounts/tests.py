from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="test_user_password",
        )

        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="test_admin",
            email="test_admin@email.com",
            password="test_admin_password",
        )

        self.assertEqual(admin_user.username, "test_admin")
        self.assertEqual(admin_user.email, "test_admin@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
