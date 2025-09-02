import unittest
import requests

BASE_URL = 'http://127.0.0.1:3000'


class TestNodeAPI(unittest.TestCase):


    def test_post_item(self):
        data = {"name":"Laptop","price":1500}
        response = requests.post(f"{BASE_URL}/items",json=data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),data)

    def test_get_items_after_post(self):
        response = requests.get(f"{BASE_URL}/items")
        self.assertEqual(response.status_code,200)
        self.assertIn({'name':"Laptop","price":1500},response.json())


if __name__ == "__main__":
    unittest.main()