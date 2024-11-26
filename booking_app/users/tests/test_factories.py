from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status

from ..factories import AccountFactory
from ..models import Account


@tag('factories')
class AccountFactoriesTest(TestCase):
    def test_account_factory_correct_create_single_object(self):
        AccountFactory.create()
        self.assertEqual(Account.objects.count(), 1)

    def test_account_factory_correct_create_batch_objects(self):
        AccountFactory.create_batch(5)
        self.assertEqual(Account.objects.count(), 5)


# python manage.py test --tag='factories'
