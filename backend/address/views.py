from rest_framework import generics, authentication \
    , permissions, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import CitySerializer, StateSerializer, \
    AddressSerializer
from address.models import State, City, Address


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
        serializer.save(user=self.request.user)
