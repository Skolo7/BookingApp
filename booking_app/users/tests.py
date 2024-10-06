from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from django.contrib.auth import get_user_model


class UserAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        # Account = get_user_model()
        # self.user1 = Account.objects.create_user(
        #     username='admin1',
        #     email='admin1@test.com',
        #     password='admin123',
        #     is_staff=True,
        #     is_active=True
        # )
        # self.user2 = Account.objects.create_user(
        #     username='Guest4',
        #     email='guest4@test.com',
        #     password='guest123',
        #     is_staff=False,
        #     is_active=True
        # )


    def test_get_user_list(self):
        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        first_user = response.data[0]
        self.assertEqual(first_user['username'], 'admin1')
        self.assertTrue(first_user['is_staff'])
        self.assertTrue(first_user['is_active'])
