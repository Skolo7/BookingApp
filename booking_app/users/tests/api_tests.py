from django.test import TestCase, tag
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from ..factories import AccountFactory
from ..models import Account


class AccountTests(APITestCase):
    def setUp(self):
        # self.client = APIClient()
        self.user = AccountFactory.create()
        # self.admin_user = Account.objects.create_superuser(
        #     username='admin',
        #     email='admin@test.com',
        #     password='password'
        # )
        self.client.force_authenticate(user=self.user)

    # GET
    def test_get_accounts_list(self):
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_accounts_list_format(self):
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_accounts_list_fields(self):
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_keys = {'username', 'first_name', 'last_name', 'email'}

        for account in data:
            self.assertEqual(set(account.keys()), expected_keys)

    def test_get_accounts_count(self):
        url = reverse('account-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(len(data), Account.objects.count())

    def test_filter_active_users(self):
        response = self.client.get('/api/v1/accounts/?is_active=true')
        data = response.json()
        for account in data:
            self.assertTrue(account['is_active'])

    # POST
    def test_create_user(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@test.com',
            'is_staff': False,
            'is_active': True,
        }
        response = self.client.post('/api/v1/accounts/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_user_no_username(self):
        # arrange
        data = {'first_name': 'New', 'last_name': 'User', 'email': 'newuser@test.com'}

        # act
        response = self.client.post('/api/v1/accounts/', data, format='json')

        # assert
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_username(self):
        # existing_user = User.objects.create(username='duplicate')
        AccountFactory.create(username='duplicate')
        data = {'username': 'duplicate', 'first_name': 'New', 'last_name': 'User'}
        response = self.client.post('/api/v1/accounts/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        data = {'username': 'newuser'}
        response = self.client.post('/api/v1/accounts/', data, format='json')
        self.assertEqual(response.status_code, 400)

    # PUT
    def test_update_user(self):
        user = AccountFactory.create()
        data = {'first_name': 'Updated'}
        response = self.client.put(f'/api/v1/accounts/{user.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')

    def test_update_user_no_username(self):
        user = AccountFactory.create()
        data = {'username': ''}
        response = self.client.put(f'/api/v1/accounts/{user.id}/', data, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_user(self):
        user = AccountFactory.create()
        response = self.client.delete(f'/api/v1/accounts/{user.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Account.objects.filter(id=user.id).exists())

    def test_delete_non_existing_user(self):
        response = self.client.delete('/api/v1/accounts/999/')
        self.assertEqual(response.status_code, 404)

    # permissions
    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get('/api/v1/accounts/')
        self.assertEqual(response.status_code, 403)

    def test_admin_access_only(self):
        self.client.logout()
        self.client.login(username='non_admin', password='password')
        response = self.client.get('/api/v1/accounts/')
        self.assertEqual(response.status_code, 403)

    def test_filter_staff_users(self):
        response = self.client.get('/api/v1/accounts/?is_staff=true')
        data = response.json()
        for account in data:
            self.assertTrue(account['is_staff'])

    def test_filter_by_joined_date(self):
        response = self.client.get('/api/v1/accounts/?date_joined_after=2024-01-01')
        data = response.json()
        for account in data:
            self.assertGreaterEqual(account['date_joined'], '2024-01-01')

    def test_invalid_url(self):
        response = self.client.get('/api/v1/invalid/')
        self.assertEqual(response.status_code, 404)

    def test_create_user_duplicate_email(self):
        user = AccountFactory.create(username='user1', email='user1@test.com')
        data = {'username': 'user2', 'email': 'user1@test.com'}
        response = self.client.post('/api/v1/accounts/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_password_length(self):
        data = {'username': 'newuser', 'password': 'short'}
        response = self.client.post('/api/v1/accounts/', data, format='json')
        self.assertEqual(response.status_code, 400)


# @tag('x')
# class AccountTestTests(APITestCase):
#     def setUp(self):
#         # self.client = APIClient()
#         self.user = AccountFactory.create()
#         # self.admin_user = Account.objects.create_superuser(
#         #     username='admin',
#         #     email='admin@test.com',
#         #     password='password'
#         # )
#         self.client.force_authenticate(user=self.user)
#
#
#     def test_get_accounts_list_fields_1(self):
#         url = reverse('account-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         expected_keys = {'username', 'first_name', 'last_name', 'email'}
#
#         for account in data:
#             self.assertEqual(set(account.keys()), expected_keys)
