from django.test import TestCase
from rest_framework.test import APIClient
from .models import Member

class MemberAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "09123456789"
        }
        self.member = Member.objects.create(**self.member_data)

    def test_create_member(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "09987654321"
        }
        response = self.client.post('/api/members/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], "Jane")

    def test_create_member_missing_fields(self):
        response = self.client.post('/api/members/', {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('phone', response.data)

    def test_update_member(self):
        data = {"first_name": "Johnny"}
        response = self.client.patch(f'/api/members/{self.member.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], "Johnny")

    def test_delete_member(self):
        response = self.client.delete(f'/api/members/{self.member.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Member.objects.filter(id=self.member.id).exists())
