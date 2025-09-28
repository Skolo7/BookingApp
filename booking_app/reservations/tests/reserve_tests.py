from datetime import timedelta
from http import HTTPStatus

from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, tag
from django.urls import reverse
from django.utils import timezone
from reservations.models import Reservation
from reservations.models.products import Desk, Room
from users.models import Account
import datetime



class TestReserveDeskView(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.another_user = Account.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )

        self.desk1 = Desk.objects.create(name="Desk 1", number=1)
        self.desk2 = Desk.objects.create(name="Desk 2", number=2)

        self.room1 = Room.objects.create(name="Room 1", number=1, max_amount_of_people=10)

        self.today = timezone.now().date()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.day_after_tomorrow = self.today + datetime.timedelta(days=2)

        self.client = Client()
        self.client.force_login(self.user)


    def test_reserve_view_get_no_filter(self):
        """
        This test checks reservation page rendering without filtering desks.
        :return:
        """
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reserve.html')
        self.assertIn('all_desks', response.context)
        self.assertIn('all_rooms', response.context)

    def test_filter_desks_by_date(self):
        """
        this test is checking filtering desks using date ranges
        :return:
        """
        params = {
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.get(reverse('reserve'), params)
        self.assertEqual(response.status_code, 200)

    def test_reserve_desk_post(self):
        """
        Test is verifying if reservation process works fine - by simulating form sending and checks if new reservation is created
        :return:
        """
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reservation.objects.filter(desk=self.desk1).exists())

    def test_reserve_room_post(self): # dla roomu
        """
        This test is checking if room reservation is working and if its correctly reserving object
        :return:
        """
        data = {
            'number': self.room1.number,
            'type': 'ROOM',
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 1)
        print("!!")
        print(vars(Reservation.objects.first()))
        print('!!')
        self.assertTrue(Reservation.objects.filter(room=self.room1).exists())


    def test_reserve_past_dates(self):
        """
        Checking if app is declining reservation attempts with past dates.
        :return:
        """
        yesterday = self.today - datetime.timedelta(days=1)
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': yesterday.strftime('%Y-%m-%d'),
            'end_date': self.today.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(desk=self.desk1, start_date=yesterday).exists())
    @tag("test2")
    def test_reserve_already_reserved_desk(self):
        """
        Test is verifying if code is preventing from double reservations of exact same objects
        """
        # Tworzenie pierwszej rezerwacji bezpośrednio przez model
        Reservation.objects.create(
            desk=self.desk1,
            person=self.user,
            start_date=self.tomorrow,
            end_date=self.day_after_tomorrow,
            type='DESK'
        )

        initial_count = Reservation.objects.filter(desk=self.desk1).count()
        self.assertEqual(initial_count, 1)

        self.client = Client(raise_request_exception=False)
        self.client.force_login(self.user)

        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data, follow=True)
        final_count = Reservation.objects.filter(desk=self.desk1).count()
        self.assertEqual(final_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_filter_unavailable_desks(self):
        """
        This test is checking of correct desk filtering which is already reserved in such dates, showing only available
        :return:
        """
        Reservation.objects.create(
            desk=self.desk1,
            person=self.user,
            start_date=self.tomorrow,
            end_date=self.day_after_tomorrow,
            type='DESK'
        )
        params = {
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.get(reverse('reserve'), params)
        self.assertNotIn(self.desk1, response.context['all_desks'])
        self.assertIn(self.desk2, response.context['all_desks'])

    def test_reserve_view_not_logged_in(self):
        """
        Testing view for logged out user
        :return:
        """
        self.client.logout()
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, 302)

    def test_filter_invalid_date(self):
        """
        Testing desk filtering with incorrect data form
        :return:
        """
        params = {
            'start_date': self.day_after_tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.today.strftime('%Y-%m-%d'),
        }
        response = self.client.get(reverse('reserve'), params)
        self.assertEqual(response.status_code, 200)
        self.assertIn('all_desks', response.context)

    def test_reserve_invalid_form(self):
        """
        Test is checking app vulnerability for invalid reservation form
        :return:
        """
        data = {
            'number': 178,
            'type': 'DESK',
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(person=self.user).exists())

    def test_reserve_end_date_before_start_date(self):
        """
        Test checks if end date is before start date and declining it if incorrect.
        :return:
        """
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': self.day_after_tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(desk=self.desk1).exists())

    def test_filter_desk_view_post(self):
        """
        Test is verifying view of desk filtering by checking if after sending filter form is getting correct redirect
        :return:
        """
        data = {
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 302)  # rzekierowanie

    def test_filter_desk_view_invalid_form(self): # do srpawdzenia
        """
        Checking how app will behave after getting incorrect data in object filtering form
        :return:
        """
        data = {
            'start_date': 'invalid-date',
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve_desk'), data)
        self.assertEqual(response.status_code, 302)





    def test_reserve_max_period(self):
        """
        Checking if app is accepting long time reservations (greater than 1 month)
        :return:
        """
        max_date = self.today + datetime.timedelta(days=31)
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': max_date.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reservation.objects.filter(desk=self.desk1).exists())

    def test_get_available_rooms(self):
        """
        Testing of getting available rooms
        :return:
        """
        Reservation.objects.create(
            room=self.room1,
            person=self.user,
            start_date=self.tomorrow,
            end_date=self.day_after_tomorrow,
            type='ROOM'
        )

        params = {
            'start_date': self.tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.get(reverse('reserve'), params)
        self.assertNotIn(self.room1, response.context['all_rooms'])

    def test_get_default_desks(self):
        """
        testing if default view is correctly showing available desks for today date
        """
        Reservation.objects.create(
            desk=self.desk1,
            person=self.user,
            start_date=self.today,
            end_date=self.today,
            type='DESK'
        )

        response = self.client.get(reverse('reserve'))
        self.assertNotIn(self.desk1, response.context['all_desks'])
        self.assertIn(self.desk2, response.context['all_desks'])


    def test_reserve_desk_different_periods(self):
        """
        Testing of reserving same desk by few users in different time ranges
        :return:
        """
        user2 = Account.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )
        Reservation.objects.create(
            desk=self.desk1,
            person=self.user,
            start_date=self.tomorrow,
            end_date=self.tomorrow,
            type='DESK'
        )
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword123')

        day_after_tomorrow = self.today + datetime.timedelta(days=2)
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': day_after_tomorrow.strftime('%Y-%m-%d'),
            'end_date': day_after_tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)

        self.assertTrue(Reservation.objects.filter(desk=self.desk1, person=user2).exists())
        self.assertEqual(Reservation.objects.filter(desk=self.desk1).count(), 2)
    def test_reserve_start_date_after_end_date(self):
        """
        Test validates date chronology in reservation process
        :return:
        """
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': self.day_after_tomorrow.strftime('%Y-%m-%d'),
            'end_date': self.tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reservation.objects.filter(desk=self.desk1).exists())


    def test_get_available_desks_method(self):
        """
        testing get_available_desks() method, verifying if its correctly filtering desks with already reserved objects.
        """
        Reservation.objects.create(
            desk=self.desk1,
            person=self.user,
            start_date=self.tomorrow,
            end_date=self.day_after_tomorrow,
            type='DESK'
        )
        from reservations.views.reserve_desk_view import ReserveDeskView
        view = ReserveDeskView()
        available_desks = view.get_available_desks(self.tomorrow, self.day_after_tomorrow)

        self.assertNotIn(self.desk1, available_desks)
        self.assertIn(self.desk2, available_desks)


    def test_error_message_for_invalid_dates(self):
        """
        Test checks if app is showing correct error codes after reservations with invalid data
        """
        yesterday = self.today - datetime.timedelta(days=1)
        data = {
            'number': self.desk1.number,
            'type': 'DESK',
            'start_date': yesterday.strftime('%Y-%m-%d'),
            'end_date': self.today.strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('reserve'), data)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Cannot reserve for past days.")


    def test_get_reserve_today_desks_unauthorized_user_redirect_to_login_page(self):
        """
        Tests that an unauthorized user attempting to access the reservation page
        is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('reserve'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')


    def test_get_reserve_today_desks(self):
        """
        Tests the retrieval of desks available for reservation today and validates the response.
        """
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'reserve.html')
        all_desks = response.context['all_desks']
        self.assertIn(self.desk1, all_desks)
        self.assertIn(self.desk2, all_desks)


    def test_get_reserve_today_returns_only_desks_which_are_not_reserved(self):
        """
        Tests that the "reserve" endpoint retrieves only desks that are not reserved
        for the current day.
        """
        today = timezone.now().date()
        Reservation.objects.create(
            desk=self.desk1, start_date=today, end_date=today, person=self.another_user
        )
        response = self.client.get(reverse('reserve'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.desk1, response.context['all_desks'])
        self.assertIn(self.desk2, response.context['all_desks'])


    def test_create_reservation_for_today(self):
        """
        This test checks both the HTTP response status and the existence of the reservation in the
        database.
        """
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
        """
        Tests creating a reservation for a past date. Ensures that the system
        does not allow reservations for dates that are in the past and verifies
        the proper error message and the absence of reservation creation.
        """
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
        """
        Tests concurrent reservation attempts for a desk and ensures that proper
        validation or error handling mechanisms are in place when attempting
        conflicting reservations.
        """
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

