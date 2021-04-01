from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """test publicly available API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ il faut se loguer pour acceder"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivaleIngredientApiTest(TestCase):
    """Test the private ingred API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'slm@i.fr',
            '12345689'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        Ingredient.objects.create(user=self.user, name='sel')
        Ingredient.objects.create(user=self.user, name='poivre')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = get_user_model().objects.create_user('autre@a.fr', '1234444444')
        ingredient = Ingredient.objects.create(user=user2, name="banane")
        Ingredient.objects.create(user=self.user, name="poire")
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertNotEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """test creation d'un ingredient"""
        payload = {'name': 'sucre'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """creation d'un ingredient invalide"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_ingredients_asssigned_to_recipes(self):
        """Test filtering tags by thiose assigned to recipes"""
        ing1 = Ingredient.objects.create(user=self.user, name='pomme')
        ing2 = Ingredient.objects.create(user=self.user, name='poire')
        recipe = Recipe.objects.create(
            title='scrambled eggs',
            time_minutes=10,
            price=1,
            user=self.user
        )
        recipe.ingredients.add(ing1)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        serializer1 = IngredientSerializer(ing1)
        serializer2 = IngredientSerializer(ing2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrice_ingredients_assignde_unqie(self):
        ing = Ingredient.objects.create(user=self.user, name='egg')
        Ingredient.objects.create(user=self.user, name='milk')
        recipe1 = Recipe.objects.create(
            title='scrambled eggs',
            time_minutes=10,
            price=1,
            user=self.user
        )
        recipe1.ingredients.add(ing)
        recipe2 = Recipe.objects.create(
            title='corn flakes',
            time_minutes=10,
            price=1,
            user=self.user
        )
        recipe2.ingredients.add(ing)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
