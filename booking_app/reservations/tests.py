from http import HTTPStatus


from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone
from pprint import pprint as pp
from .models import Desk, Reservation
from users.models import Account
from resources.scripts.products import create_desks, create_parking_spots, create_rooms

class TestReserveDeskView(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(username='test@user.com', password='Qwerty123!')
        create_desks()
        # create_parking_spots()
        # create_rooms()

    def test_get_reserve_today_desks_unauthorized_user(self):
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

    def test_get_reserve_today_returns_only_desks_which_are_not_reserved(self):
        self.client.force_login(self.user)
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        desk1 = Desk.objects.get(number=1)
        desk2 = Desk.objects.get(number=2)
        Reservation.objects.create(desk=desk1, start_date=today, end_date=tomorrow)
        Reservation.objects.create(desk=desk2, start_date=today, end_date=tomorrow)
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'reserve.html')
        all_desks = response.context['all_desks']
        number_of_desks = len(all_desks)
        self.assertEqual(number_of_desks, 28)
        self.assertNotIn(desk1, all_desks)
        self.assertNotIn(desk2, all_desks)

    def test_get_available_desks