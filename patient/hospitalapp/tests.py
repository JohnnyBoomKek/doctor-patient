from django.http import response
from django.test import TestCase, Client

# Create your tests here.


class Test(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def smoke_screen_test(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_list_of_patients(self):
        pass