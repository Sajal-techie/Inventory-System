from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from item_app.models import Item
from auth_app.models import User


class ItemViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='test_email@gmail.com', password='test_password')
        self.token = self.get_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.item = Item.objects.create(name='Test Item', description='Test Description')
        self.url = reverse('items-list')
        self.detail_url = reverse('items-detail', kwargs={'pk': self.item.pk})
        
    def tearDown(self) -> None:
        cache.clear()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_list_items(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_item(self):
        data = {'name': 'New Item', 'description': 'New Description'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
    
    def test_retrieve_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)
    
    def test_update_item(self):
        data = {'name': 'Updated Item', 'description':'Updated description'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")
    
    def test_delete_item(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_jwt_authentication_required(self):
        self.client.credentials()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"name": "New Item", "description": "New Description"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"name": "Updated Item", "description": "Updated Description"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZAION="Bearer Invalid_Token")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_cache_on_retrieve(self):
        response1 = self.client.get(self.detail_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        cached_item = cache.get(f'item_{self.item.pk}')
        self.assertIsNotNone(cached_item)

        Item.objects.filter(pk=self.item.pk).update(name='Modified Name')

        response2 = self.client.get(self.detail_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['name'], "Test Item")
    
    def test_cache_invalidation_on_update(self):
        self.client.get(self.detail_url)

        data = {'name': 'Updated Item', 'description': "Updated Description"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cached_item = cache.get(f'item_{self.item.pk}')
        self.assertIsNone(cached_item)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Item")
    
    def test_cache_invalidation_on_delete(self):
        self.client.get(self.detail_url)
        cached_item = cache.get(f'item_{self.item.pk}')
        self.assertIsNotNone(cached_item)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        cached_item = cache.get(f'item_{self.item.pk}')
        self.assertIsNone(cached_item)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item_already_exists(self):
        data = {'name': "Test Item", 'description': "Duplicate Name"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_non_existent_item(self):
        invalid_url = reverse('items-detail', kwargs={'pk': 999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)