from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

Account = get_user_model()


class TestUserAccountView(TestCase):
    def setUp(self):
        self.admin_user = Account.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        self.normal_user = Account.objects.create_user(
            username='normaluser',
            email='normal@example.com',
            password='normal123',
            first_name='Normal',
            last_name='User'
        )
        self.inactive_user = Account.objects.create_user(
            username='inactiveuser',
            email='inactive@example.com',
            password='inactive123',
            first_name='Inactive',
            last_name='User',
            is_active=False
        )

        self.today = timezone.now().date()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.client = Client()

    def test_login_view_get(self): #err
        """
        Tests that login page loads correctly with proper template
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


    def test_login_successful(self):
        """
        Tests successful login attempt and proper redirection after login
        """
        data = {
            'username': 'normaluser',
            'password': 'normal123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('index'))


    def test_login_invalid_credentials(self): # error
        """
        Tests login attempt with invalid credentials
        """
        data = {
            'username': 'normaluser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')


    def test_login_inactive_user(self): # error
        """
        Tests login attempt with inactive user account
        """
        data = {
            'username': 'inactiveuser',
            'password': 'Start123!@'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account is inactive')


    def test_logout(self):
        """
        Tests user logout functionality
        """
        self.client.login(username='normaluser', password='Start123!@')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('users/logout/'))


    def test_profile_view_authenticated(self):
        """
        Tests that authenticated users can access their profile
        """
        self.client.force_login(user=self.normal_user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')


    def test_profile_view_unauthenticated(self):
        """
        Tests that unauthenticated users are redirected to login page
        """
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")


    def test_update_profile(self):
        """
        Tests user profile update functionality
        """
        self.client.force_login(user=self.normal_user)
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.post(reverse('profile'), data)
        self.assertRedirects(response, reverse('profile'))
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.first_name, 'Updated')
        self.assertEqual(self.normal_user.last_name, 'Name')
        self.assertEqual(self.normal_user.email, 'updated@example.com')

    def test_update_profile_invalid_data(self): # czy user jest zalogowany
        """
        Tests profile update with invalid data
        """
        self.client.force_login(user=self.normal_user)
        data = {
            'email': 'invalid-email'
        }
        response = self.client.post(reverse('profile'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter an email address')


    def test_change_password(self): # error
        """
        Tests password change functionality
        """
        self.client.login(username='normaluser', password='Start123!@')
        data = {
            'old_password': 'Start123!@',
            'new_password1': 'Start123!@Start123!@',
            'new_password2': 'Start123!@Start123!@'
        }
        response = self.client.post(reverse('password_change'), data)
        self.assertRedirects(response, reverse('password_change_done'))

        self.client.logout()
        login_successful = self.client.login(username='normaluser', password='newPassword123')
        self.assertTrue(login_successful)


    def test_change_password_incorrect_old(self):
        """
        Tests password change with incorrect old password
        """
        self.client.force_login(user=self.normal_user)
        data = {
            'old_password': 'Start123!',
            'new_password1': 'Start123!@Start123!@',
            'new_password2': 'Start123!@Start123!@'
        }
        response = self.client.post(reverse('password_change'), data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_mismatch(self):
        """
        Tests password change with mismatched new passwords
        """
        self.client.force_login(user=self.normal_user)
        data = {
            'old_password': 'Start123!@',
            'new_password1': 'Start123!@Start123!@',
            'new_password2': 'Start123!@Start123!@Start123!@'
        }
        response = self.client.post(reverse('password_change'), data)
        self.assertEqual(response.status_code, 200)

    def test_register_view_get(self):
        """
        Tests that registration page loads correctly
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_successful(self):
        """
        Tests successful registration and account creation
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Start123!@',
            'password2': 'Start123!@',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Account.objects.filter(username='newuser').exists())
    def test_register_username_exists(self):
        """
        Tests registration with already existing username
        """
        data = {
            'username': 'normaluser',
            'email': 'another@example.com',
            'password1': 'Start123!@',
            'password2': 'Start123!@'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)

    def test_register_email_exists(self):
        """
        Tests registration with already existing email
        """
        data = {
            'username': 'anotheruser',
            'email': 'normal@example.com',
            'password1': 'Start123!@',
            'password2': 'Start123!@'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_password_too_short(self):
        """
        Tests registration with password that is too short
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'pass',
            'password2': 'pass'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
    def test_register_password_mismatch(self):
        """
        Tests registration with mismatched passwords
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Start123!@',
            'password2': 'Start1234!@'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)


    def test_admin_dashboard_access(self):
        """
        Tests access to admin dashboard for superuser
        """
        self.client.login(username='adminuser', password='admin123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_access_denied(self):
        """
        Tests that regular users cannot access admin dashboard
        """
        self.client.login(username='normaluser', password='Start123!@')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_view(self):
        """
        Tests password reset view renders correctly
        """
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
