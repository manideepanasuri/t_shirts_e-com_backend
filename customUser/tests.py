from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(phone="9494358750",name="Manideep", password="foo")
        self.assertEqual(user.name, "Manideep"),
        self.assertEqual(user.phone, "9494358750")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(phone="",name="Manideep")
        with self.assertRaises(ValueError):
            User.objects.create_user(phone="",name="Manideep", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(phone="9494358751",name="Manideep", password="foo")
        self.assertEqual(admin_user.phone, "9494358751")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone="9494358750",name="Manideep", password="foo", is_superuser=False)