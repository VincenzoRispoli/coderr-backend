from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class ReviewsTests(APITestCase):
    def test_get_review(self):
        url = "http://127.0.0.1:8000/api/reviews/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)