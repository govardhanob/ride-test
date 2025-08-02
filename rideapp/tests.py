# rideapp/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TestRideSharingAPI(APITestCase):
    def test_register_login_create_ride(self):
        register_url = reverse('register-list')  # For viewsets, use '-list' for POST
        login_url = reverse('token_obtain_pair')
        ride_url = reverse('ride-list')

        # Register a user
        register_data = {
            "username": "testuser",
            "password": "testpass123",
            "role": "rider"
        }
        response = self.client.post(register_url, register_data, format='json')
        print("REGISTER RESPONSE:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "testpass123",
            "latitude":9.9816,
            "longitude":76.2999
        }
        response = self.client.post(login_url, login_data, format='json')
        print("LOGIN RESPONSE:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create ride
        ride_data = {
            "pickup_latitude": 10.543,
            "pickup_longitude": 76.987,
            "dropoff_latitude": 10.545,
            "dropoff_longitude": 76.989
            }

        response = self.client.post(ride_url, ride_data, format='json')
        print("CREATE RIDE RESPONSE:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
