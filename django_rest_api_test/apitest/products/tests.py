from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {'name':'Whey Protein','price':'1200.50'}

    def test_create_product(self):
        response = self.client.post('/api/products/',self.product_data,format='json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['name'],'Whey Protein')


    def test_get_products(self):
        Product.objects.create(name='Creatine',price=900)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code,200)
        self.assertGreater(len(response.data),0)