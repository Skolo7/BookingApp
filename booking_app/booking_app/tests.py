from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from reservations.models import Desk, Reservation
from pprint import pprint as pp

class TestReserveView(TestCase):
    def setUp(self) -> None:
        pass
        # TODO Utworzenie usera i zalgoowanie się self.clientem przed wykonaniem get.

    # def test_get_reserve_today_desks_unauthorized_user(self):
    #     response = self.client.get(reverse('reserve'))
    #     self.assertEqual(response.status_code, 403)
    #     print(response)

    def test_get_reserve_today_desks(self):
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reserve.html')
        number_of_desks = len(response.context['all_desks'])
        self.assertEqual(number_of_desks, 30)


    def test_get_reserve_today_desks_with_some_desks(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        desk1 = Desk.objects.get(number=1)
        desk2 = Desk.objects.get(number=2)
        Reservation.objects.create(desk=desk1, start_date=today, end_date=tomorrow)
        Reservation.objects.create(desk=desk2, start_date=today, end_date=tomorrow)
        response = self.client.get(reverse('reserve'))
        self.assertTemplateUsed(response, 'reserve.html')
        self.assertEqual(response.status_code, 200)
        all_desks = response.context['all_desks']
        number_of_desks = len(all_desks)
        self.assertEqual(number_of_desks, 28)
        self.assertNotIn(desk1, all_desks)
        self.assertNotIn(desk2, all_desks)