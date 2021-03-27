from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
	"""retuens recipe detail +urL"""
	return reverse('recipe:recipe-detail',args=[recipe_id])

def sample_recipe(user, **params):
	"""utility fucntion to create and return a sample recipe"""
	defaults = {
	'title': 'sampleRecipe',
	'time_minutes': 5,
	'price': 5.05,
	}
	defaults.update(params)

	return Recipe.objects.create(user=user, **defaults)

def sample_tag(user, name="testtag"):
	"""create and retrune a tag"""
	return Tag.objects.create(user=user,name=name)

def sample_ingredient(user,name='tets'):
	return Ingredient.objects.create(user=user,name=name)


class PublicRecipeApiTest(TestCase):
    """test publicly available API access"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ il faut se loguer pour acceder"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivatRecipeApiTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'x@y.fr','12345678')
		self.client.force_authenticate(self.user)

	def test_retrive_recipe(self):
		sample_recipe(user=self.user)
		sample_recipe(user=self.user)
		res = self.client.get(RECIPES_URL)
		recipes = Recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)


	def test_recipes_limited_to_user(self):
		user2 = get_user_model().objects.create_user(
			'autre@y.fr','45678456')
		sample_recipe(user=user2)
		sample_recipe(user=self.user)

		res= self.client.get(RECIPES_URL)
		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes,many=True)

		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(len(res.data),1)
		self.assertEqual(res.data,serializer.data)

	def test_view_recipe_details(self):
		"""viewing a recipe detail"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		recipe.ingredients.add(sample_ingredient(user=self.user))
		url = detail_url(recipe.id)
		res = self.client.get(url)

		serializer= RecipeDetailSerializer(recipe)

		self.assertEqual(res.data, serializer.data)