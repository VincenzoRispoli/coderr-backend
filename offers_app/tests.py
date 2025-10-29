from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer


class OfferTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="Joe", password="joe123")
        self.offer = Offer.objects.create(user=self.user, title="Offer 1", description="The first offer of the history", image=None, min_price=2000, min_delivery_time=2)
    
    def test_offers_detail(self):
        url = reverse("offer-detail", kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        expexted_data = OfferSerializer(self.offer).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expexted_data)
        self.assertContains(response, 'title')
