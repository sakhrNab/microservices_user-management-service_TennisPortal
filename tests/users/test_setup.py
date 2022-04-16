from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('apps.manage_user:register')
        self.login_url=reverse('apps.manage_user:token_obtain_pair')

        self.user={
            'email':'example1@gmail.com',
            'username':'zackazico',
            'password':'apple_2001',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'pk': 2,

            "gender": "Other",
            "age": "43",
            "country": "DE",
            "city": "Berlin",
            "region": "Frankfurt",
            "zip_code": "11111",
            "skill_level": "Advanced Beginner",
            "phone_number": "4916319787",
            "game_type": "Tennis",
            "address": "Derf"
        }
        self.user_short_password={
            'email':'example1@gmail.com',
            'username':'zackazico',
            'password1':'password',
            'password2':'password', 
            'first_name': 'first_name',
            'last_name': 'last_name',
        }
        self.user_unmatching_password={
            'email':'example1@gmail.com',
            'username':'zackazico',
            'password1':'password',
            'password2':'password', 
            'first_name': 'first_name',
            'last_name': 'last_name',
        }

        self.user_invalid_email={
            'email':'example1@gmail.com',
            'username':'zackazico',
            'password1':'password',
            'password2':'password', 
            'first_name': 'first_name',
            'last_name': 'last_name',
        }

        self.valid_payload = {
            'old_password': 'apple_2001',
            'new_password1': 'apple_20011',
            'new_password2': 'apple_20011',
        }
        self.invalid_payload = {
            'old_password': 'apple_2001',
            'new_password1': 'apple11',
            'new_password2': 'apple_20011',
        }

        self.valid_payload = {
            'old_password': 'apple_2001',
            'new_password1': 'apple_20011',
            'new_password2': 'apple_20011',
        }
        self.invalid_payload = {
            'old_password': 'apple_2001',
            'new_password1': 'apple11',
            'new_password2': 'apple_20011',
        }
        return super().setUp()

