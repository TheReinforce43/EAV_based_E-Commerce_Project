# apps/users/tests/test_models.py
from django.test import TestCase
from apps.users.models import User

class UserModelTest(TestCase):

    def setUp(self):
        # runs before EVERY test method in this class
        self.user = User.objects.create_user(
            email="test@example.com",
            first_name="Rahim",
            password="strongpass123"
        )

    def test_user_str_returns_email(self):
        self.assertEqual(str(self.user), "test@example.com")

    def test_user_default_type_is_customer(self):
        self.assertEqual(self.user.user_type, "customer")

    def test_user_email_is_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="tesft@example.com",  # duplicate
                first_name="Another",
                password="pass456"
            )