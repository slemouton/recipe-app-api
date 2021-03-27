from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='lemouton@ircam.fr', password='123456'):
    """cree un utilisateur de test"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """test creating a nouvel user avec email"""
        email = 'test@truc.fr'
        password = '123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """check email case insensitive"""
        email = 'test@TEST.FR'
        user = get_user_model().objects.create_user(email, 'testtest')
        self.assertEqual(user.email, email.lower())

    def test_email_is_valid(self):
        """creating a user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_superuser_is_created(self):
        """test creating a new su"""
        user = get_user_model().objects.create_superuser(
            'test@x.fr',
            'test123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name = 'Vegan')

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """"test les ingredinent chainne"""
        ingredient=models.Ingredient.objects.create(
            user=sample_user(),
            name='farine'
            )

        self.assertEquals(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """test la represetnation en chaine de caractere de l'objet recette"""
        recipe=models.Recipe.objects.create(
            user=sample_user(),
            title='nockedli',
            time_minutes = 5,
            price=5.00)

        self.assertEqual(str(recipe),recipe.title)