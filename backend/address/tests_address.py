from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from address.models import Address, State, City
from address.serializers import AddressSerializer

ADDRESS_URL = reverse('address:address-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

    
def sample_state(**params):
    """Create a state"""
    return State.objects.create(
        name= 'Santa Catarina',
        init= 'SC'
    )

def sample_city(**params):
    state = sample_state()
    return City.objects.create(
        name='Florianopolis',
        state= state
    )

def sample_address(user, **params):        
    city = sample_city()
    """Returns a sample address"""
    defaults = {
        'street': 'Rua da Silva',
        'number': '01',
        'zip': '990000',
        'city': city
    }
    defaults.update(params)
    return Address.objects.create(user=user, **defaults)


class PublicAddressApiTests(TestCase):
    """Tests if address can be included """
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        res = self.client.get(ADDRESS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTests(TestCase):
    """Test authorized user address API"""
    
    def setUp(self):

        self.user = create_user(
            email='test@haupai.com',
            password='123456',
            name='Test'           
        )        
        self.client = APIClient()        
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        """Test create address with current user"""
        address_new = sample_address(user=self.user)
        res = self.client.get(ADDRESS_URL)

        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(address_new.user, self.user)