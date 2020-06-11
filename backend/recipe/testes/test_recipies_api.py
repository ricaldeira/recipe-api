from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """REturn recipe detail irl"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='Main course'):
    """Create sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='cabbage'):
    """Create sample ingrediente"""
    return Ingredient.objects.create(user=user, name=name)

def sample_recipe(user, **params):
    """Return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': '10',
        'price': '5.00',
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)



class PublicRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Teste that authentication is required"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Teste unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'teste@haupai.com',
            'testePass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipies(self):
        """Test retrieving a list of recipies"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Teste retrieving recipies for user"""
        user2 = get_user_model().objects.create_user(
            'test2@haupai.com',
            'pass2'
        )
        sample_recipe(self.user)
        sample_recipe(user2)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    
    def test_view_recipe_detail(self):
        """Test viewing  recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Teste creating recipe"""
        payload = {
            'title': 'Cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        
    def test_create_recipe_with_tags(self):
        """Test creating recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Desert')
        payload = {
            'title': 'Avocado lime cheescake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 15.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
    
    def test_create_recipe_with_ingredients(self):
        """Test wth ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')
        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 40,
            'price': 25.00
        }
        res = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
        
