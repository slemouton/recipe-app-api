from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """test creating a nouvel user avec email"""
        email = 'test@truc.fr'
        password = '123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
            )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """check email case insensitive"""
        email = 'test@TEST.FR'
        user = get_user_model().objects.create_user(email,'testtest')
        self.assertEqual(user.email,email.lower())

    def test_email_is_valid(self):
        """creating a user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_superuser_is_created(self):
        """test creating a new su"""
        user = get_user_model().objects.create_superuser(
            'test@x.fr',
            'test123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
