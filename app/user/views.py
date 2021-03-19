from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import AuthTokenSerializer

from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
	"""create a nouvel utilisateur dans le systeme"""
	serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
	""" create a new auth tokeb for user"""
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

