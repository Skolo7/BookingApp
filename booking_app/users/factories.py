import factory

from .models import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


# AccountFactory.create()
# self.assert(Account.objects.count(), 1)
# AccountFactory.create_batch(5)
# self.assert(Account.objects.count(), 5)
#
#
