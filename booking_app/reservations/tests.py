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

    def test_rendering_of_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reserve.html')

    @tag('x')
    def test_form_submission(self):
        self.client.force_login(self.user)
        data = {'start_date': '2023-01-01', 'end_date': '2023-01-10'}
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reserve.html')
        self.assertEqual(Reservation.objects.count(), 1)


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


