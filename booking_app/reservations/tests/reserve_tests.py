from datetime import timedelta
from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone
from reservations.models import Desk, Reservation
from reservations.views import ReserveDeskView
from resources.scripts.products import create_desks
from users.models import Account


class TestReserveDeskView(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            username='test@user.com', password='Qwerty123!'
        )
        create_desks()
        # create_parking_spots()
        # create_rooms()

    def test_get_reserve_today_desks_unauthorized_user_redirect_to_login_page(self):
        response = self.client.get(reverse('reserve'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_reserve_today_desks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'reserve.html')
        number_of_desks = len(response.context['all_desks'])
        self.assertEqual(number_of_desks, 30)

    #
    def test_get_reserve_today_returns_only_desks_which_are_not_reserved(self):
        self.client.force_login(self.user)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        desk1 = Desk.objects.get(number=1)
        desk2 = Desk.objects.get(number=2)
        Reservation.objects.create(
            desk=desk1, start_date=today, end_date=tomorrow, person=self.user
        )
        Reservation.objects.create(
            desk=desk2, start_date=today, end_date=tomorrow, person=self.user
        )
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'reserve.html')
        all_desks = response.context['all_desks']
        number_of_desks = len(all_desks)
        self.assertEqual(number_of_desks, 28)
        self.assertNotIn(desk1, all_desks)
        self.assertNotIn(desk2, all_desks)

    #
    def test_rendering_of_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reserve.html')

    #
    # @tag('x')
    # def test_form_submission(self):
    #     self.client.force_login(self.user)
    #     data = {'start_date': '2023-01-01', 'end_date': '2023-01-10'}
    #     response = self.client.post(reverse('reserve'), data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'reserve.html')
    #     self.assertEqual(Reservation.objects.count(), 1)
    #
    def test_get_default_desks(self):
        self.client.force_login(self.user)
        today = timezone.now().date()
        default_desks = ReserveDeskView.get_default_desks(today)
        self.assertEqual(len(default_desks), 30)
        self.assertIn(Desk.objects.first(), default_desks)
        self.assertIn(Desk.objects.last(), default_desks)

    # def test_default_date_in_form(self):
    #     response = self.client.get(reverse('reserve'), data)
    #     default_date = response.context['today']
    #
    #     self.assertEqual(default_date, date_form.fields['start_date'].initial)
    #     self.assertEqual(default_date, date_form.fields['end_date'].initial)


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

    @tag('test3')
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
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("Cant reserve for past days", response.context['messages'])

    def test_concurrent_reservation_attempts(self):
        from icecream import ic

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
