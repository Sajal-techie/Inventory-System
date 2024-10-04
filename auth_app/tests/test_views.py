from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_app.models import User


class AuthViewTests(APITestCase):
    def setUp(self) -> None:
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@gmail.com'
        }
        self.invalid_user_data = {
            'username': '',
            'password': '11',
            'email':'invalid'
        }

        self.login_url = reverse('login')
        self.register_url = reverse('register')

        self.url = User.objects.create_user(
            username='newuser',
            password='newpassword',
            email='newemail@gmail.com'
        )

    def tearDown(self):
        User.objects.all().delete()
        
    def test_successful_user_registration(self):
        response = self.client.post(self.register_url, self.valid_user_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_registration_with_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)  
        self.assertIn('email', response.data)    

    def test_registration_with_missing_data(self):
        incomplete_data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)  
    
    def test_successful_user_login(self):
        login_data = {
            'email': 'newemail@gmail.com',
            'password': 'newpassword'
        }
        response = self.client.post(self.login_url,login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  
    
    def test_login_with_incorrect_credentials(self):
        invalid_login_data = {
            'email': 'newemail@gmail.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_with_missing_password(self):
        missing_data = {
            'email': 'newemail@gmail.com'
        }
        response = self.client.post(self.login_url, missing_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data) 
    
    def test_login_with_missing_email(self):
        missing_data = {
            'password':'newuser'
        }
        response = self.client.post(self.login_url, missing_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data) 