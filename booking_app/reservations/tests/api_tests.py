from django.test import TestCase, tag
from django.urls import reverse
from reservations.models.reservations import Reservation
from resources.scripts.products import create_desks
from rest_framework import status
from rest_framework.test import APIClient
from users.models import Account

from ..models import Reservation


class ReservationsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin_user = Account.objects.create_user(
            username='admin', email='admin@test.com', password='password'
        )
        self.normal_user = Account.objects.create_user(
            username='user', email='user@test.com', password='password'
        )
        create_desks()
        # self.client.force_authenticate(user=self.admin_user)
        # self.client.force_authenticate(user=self.normal_user)

    def test_get_reservations_list(self):
        self.client.force_authenticate(user=self.admin_user)
        # headers = {'Beaer token'}
        response = self.client.get(reverse('reservation-list'))
        print(response.json())
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservations_list_format(self):
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_get_reservations_list_fields(self):
        response = self.client.get(reverse('reservation-list'))
        data = response.json()
        for reservation in data:
            self.assertIn('start_date', reservation)
            self.assertIn('end_date', reservation)
            # self.assertIn('created_at', reservation)
            # self.assertIn('desk', reservation)
            # self.assertIn('room', reservation)
            # self.assertIn('parking', reservation)
            # self.assertIn('title', reservation)
            # self.assertIn('description', reservation)
            self.assertIn('person', reservation)
            self.assertIn('type', reservation)

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'start_date': '2024-11-24',
            'end_date': '2024-11-24',
            'person': self.normal_user.id,
            'title': 'Test Reservation',
            'description': 'A test reservation.',
            'type': Reservation.ReservationTypes.DESK,
        }
        response = self.client.post(reverse('reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_no_start_date(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'end_date': '2024-11-24',
            'person': self.normal_user.id,
            'title': 'Test Reservation',
            'description': 'A test reservation.',
            'type': Reservation.ReservationTypes.DESK,
        }
        response = self.client.post(reverse('reservation-list'), data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_invalid_dates(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'start_date': '2024-11-24',
            'end_date': '2024-11-23',
            'person': self.normal_user.id,
            'title': 'Test Reservation',
            'description': 'A test reservation.',
            'type': Reservation.ReservationTypes.DESK,
        }
        response = self.client.post(reverse('reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('test2')
    def test_update_reservation(self):
        self.client.force_authenticate(user=self.normal_user)
        reservation = Reservation.objects.create(
            start_date='2024-11-24',
            end_date='2024-11-24',
            person=self.normal_user.id,
        )
        data = {'title': 'Updated Title'}
        response = self.client.put(
            f'/api/v1/reservations/{reservation.id}/', data, format='json'
        )  # reverse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation.refresh_from_db()
        self.assertEqual(reservation.title, 'Updated Title')

    def test_update_reservation_invalid_dates(self):
        reservation = Reservation.objects.create(
            start_date='2024-10-01', end_date='2024-10-02', person=1
        )
        data = {'start_date': '2024-10-03', 'end_date': '2024-10-01'}
        response = self.client.put(
            f'/api/v1/reservations/{reservation.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reservation(self):
        reservation = Reservation.objects.create(
            start_date='2024-10-01', end_date='2024-10-02', person=1
        )
        response = self.client.delete(f'/api/v1/reservations/{reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())

    def test_delete_non_existing_reservation(self):
        response = self.client.delete('/api/v1/reservations/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_only(self):
        self.client.logout()
        self.client.login(username='non_admin', password='password')
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_reservations_by_person(self):
        response = self.client.get('/api/v1/reservations/?person=1')
        data = response.json()
        for reservation in data:
            self.assertEqual(reservation['person'], 1)

    def test_filter_reservations_by_date(self):  # na datetime, zobacz co jest w data.
        response = self.client.get('/api/v1/reservations/?start_date=2024-10-01')
        data = response.json()
        for reservation in data:
            self.assertGreaterEqual(reservation['start_date'], '2024-10-01')
