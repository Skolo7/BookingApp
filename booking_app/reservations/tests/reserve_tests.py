from datetime import timedelta
from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from reservations.models import Desk, Reservation
from users.models import Account


class TestReserveDeskView2(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            username='testuser', password='password123'
        )
        self.another_user = Account.objects.create_user(
            username='anotheruser', password='password456'
        )
        self.desk1 = Desk.objects.create(name="Desk 1", number=1)
        self.desk2 = Desk.objects.create(name="Desk 2", number=2)
        self.client.force_login(self.user)

    def test_get_reserve_today_desks_unauthorized_user_redirect_to_login_page(self):
        self.client.logout()
        response = self.client.get(reverse('reserve'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_reserve_today_desks(self):
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'reserve.html')
        all_desks = response.context['all_desks']
        self.assertIn(self.desk1, all_desks)
        self.assertIn(self.desk2, all_desks)

    def test_get_reserve_today_returns_only_desks_which_are_not_reserved(self):
        today = timezone.now().date()
        Reservation.objects.create(
            desk=self.desk1, start_date=today, end_date=today, person=self.another_user
        )
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.desk1, response.context['all_desks'])
        self.assertIn(self.desk2, response.context['all_desks'])

    def test_create_reservation_for_today(self):
        today = timezone.now().date()
        response = self.client.post(
            reverse('reserve'),
            {
                'number': self.desk1.number,
                'type': 'desk',
                'start_date': today,
                'end_date': today,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Reservation.objects.filter(desk=self.desk1, person=self.user).exists()
        )

    def test_create_reservation_for_past_date(
        self,
    ):
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.post(
            reverse('reserve'),
            {
                'number': self.desk1.number,
                'type': 'desk',
                'start_date': past_date,
                'end_date': past_date,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertIn(
            "Cannot reserve for past days", str(list(response.context['messages'])[0])
        )
        self.assertEqual(Reservation.objects.count(), 0)

    def test_concurrent_reservation_attempts(self):
        today = timezone.now().date()
        Reservation.objects.create(
            desk=self.desk1, start_date=today, end_date=today, person=self.another_user
        )
        response = self.client.post(
            reverse('reserve'),
            {
                'number': self.desk1.number,
                'type': 'desk',
                'start_date': today,
                'end_date': today,
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        messages = list(response.context['messages'])
        ic(messages)
        ic()
        ic()
        messages = list(get_messages(response.wsgi_request))
        ic(messages)
