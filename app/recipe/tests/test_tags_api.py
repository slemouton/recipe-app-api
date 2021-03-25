from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """ test les tag public"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'x@y.fr'
            'passxord12345')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieving tags"""
        Tag.objects.create(user=self.user, name = "Vegetarien")
        Tag.objects.create(user=self.user, name = "dessert")
        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual (res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = get_user_model().objects.create_user('autre@a.fr','1234444444')
        tag = Tag.objects.create(user=user2,name="Fruits")
        Tag.objects.create(user=self.user, name = "dessert")
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertNotEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """test creation d'un tag"""
        payload = {'name': 'Test Tag'}
        self.client.post(TAGS_URL,payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']).exists()
        self.assertTrue(exists)

    def test_crzate_tag_invaid(self):
        """creation d'un tag invalide"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)



