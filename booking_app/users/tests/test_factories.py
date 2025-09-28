from django.test import TestCase
from django.test.utils import tag
from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute, Sequence, post_generation

from users.models import Account
from ..factories import AccountFactory


@tag('factories')
class AccountFactoriesTest(TestCase):
    """
    Tests for the Account factory
    """

    def test_account_factory_correct_create_single_object(self):
        """
        Tests that a single Account object is correctly created
        """
        AccountFactory.create()
        self.assertEqual(Account.objects.count(), 1)

    def test_account_factory_correct_create_batch_objects(self):
        """
        Tests that multiple Account objects are correctly created with create_batch
        """
        AccountFactory.create_batch(5)
        self.assertEqual(Account.objects.count(), 5)

    def test_account_factory_default_values(self):
        """
        Tests that Account factory creates an object with proper default values
        """
        account = AccountFactory.create()
        self.assertTrue(account.is_active)
        self.assertTrue(account.check_password('password123'))
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_account_factory_custom_values(self):
        """
        Tests that Account factory respects custom values when provided
        """
        account = AccountFactory.create(
            username='custom_user',
            email='custom@example.com',
            first_name='Custom',
            last_name='User',
            is_staff=True
        )
        self.assertEqual(account.username, 'custom_user')
        self.assertEqual(account.email, 'custom@example.com')
        self.assertEqual(account.first_name, 'Custom')
        self.assertEqual(account.last_name, 'User')
        self.assertTrue(account.is_staff)

    def test_account_factory_unique_usernames(self):
        """
        Tests that Account factory creates unique usernames for multiple objects
        """
        accounts = AccountFactory.create_batch(3)
        usernames = [account.username for account in accounts]
        self.assertEqual(len(usernames), len(set(usernames)), "Usernames should be unique")

    def test_account_factory_email_based_on_username(self):
        """
        Tests that Account factory creates email based on username attribute
        """
        account = AccountFactory.create(username='special_user')
        self.assertEqual(account.email, 'special_user@example.com')

    def test_account_factory_password_is_set(self):
        """
        Tests that Account factory properly sets and hashes the password
        """
        account = AccountFactory.create(password='custom_password')
        self.assertTrue(account.check_password('custom_password'))

    def test_account_factory_staff_user(self):
        """
        Tests that Account factory can create staff users
        """
        staff_user = AccountFactory.create(is_staff=True)
        self.assertTrue(staff_user.is_staff)
        self.assertFalse(staff_user.is_superuser)

    def test_account_factory_superuser(self):
        """
        Tests that Account factory can create superusers
        """
        superuser = AccountFactory.create(is_staff=True, is_superuser=True)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_account_factory_inactive_user(self):
        """
        Tests that Account factory can create inactive users
        """
        inactive_user = AccountFactory.create(is_active=False)
        self.assertFalse(inactive_user.is_active)

    def test_account_factory_full_name(self):
        """
        Tests that Account factory creates users with proper first and last names
        """
        account = AccountFactory.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(account.first_name, 'John')
        self.assertEqual(account.last_name, 'Doe')

    def test_account_factory_faker_name(self):
        """
        Tests that Account factory creates users with faker-generated names
        """
        account = AccountFactory.create()
        self.assertIsNotNone(account.first_name)
        self.assertIsNotNone(account.last_name)
        self.assertNotEqual(account.first_name, '')
        self.assertNotEqual(account.last_name, '')

    def test_account_factory_sequence_username(self):
        """
        Tests that Account factory creates sequenced usernames
        """
        accounts = AccountFactory.create_batch(2)
        self.assertIn('user_0', accounts[0].username)
        self.assertIn('user_1', accounts[1].username)

    def test_account_factory_email_normalization(self):
        """
        Tests that Account factory properly normalizes email addresses
        """
        account = AccountFactory.create(email='Test@Example.COM')
        self.assertEqual(account.email, 'Test@example.com')


