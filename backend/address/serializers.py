from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import BusinessUser, Address, City, State


class StateSerializer(serializers.ModelSerializer):
    # cities = CitySerializer(many=True)
    class Meta:
        model = State
        fields = ('name', 'init')
        read_only_fields = ('id',)


class CitySerializer(serializers.ModelSerializer):

    state = StateSerializer
    class Meta:
        model = City
        fields = ('name', 'state')
        read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer    
    class Meta:
        model = Address
        fields = ['street', 'number', 'zip', 'city']
        read_only_fields = ('id',)
