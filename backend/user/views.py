from rest_framework import generics, authentication, \
    permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, AuthTokenSerializer 
from .serializers import CitySerializer, StateSerializer, \
    AddressSerializer
from core.models import State, City, Address

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class StateViewSet(generics.CreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AddressListViewSet(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin
                    ):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,) 

    def perform_create(self, serializer):
        serializer.save(user=self.requests.user)
