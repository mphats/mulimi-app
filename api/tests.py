from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class ApiJwtTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="farmer", password="pass1234")
        self.user.profile.role = "FARMER"
        self.user.profile.save()
        res = self.client.post("/api/v1/auth/token", {"username":"farmer","password":"pass1234"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.access = res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_diagnosis(self):
        res = self.client.post("/api/v1/ai-diagnosis", {"cropType":"maize","symptoms":"yellow spots"}, format="json")
        self.assertEqual(res.status_code, 200)

    def test_advice(self):
        res = self.client.post("/api/v1/farming-advice",
                               {"location":{"lat":-13.9,"lng":33.7},"cropType":"maize","season":"rainy"},
                               format="json")
        self.assertEqual(res.status_code, 200)

    def test_market(self):
        res = self.client.post("/api/v1/market-analysis", {"cropType":"maize","district":"Lilongwe","quantity":100}, format="json")
        self.assertEqual(res.status_code, 200)
