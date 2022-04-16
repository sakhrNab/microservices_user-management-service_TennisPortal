# import json
# from apps.profiles.serializers import ProfileSerializer
# from rest_framework import status
# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.contrib import auth
# from django.db.models import Q, Count
# from apps.manage_user.controller.serializers\
#     .profile_management.serializers import \
#     UserSerializer, WishListSerializer
#
# from apps.profiles.models import Profile
#
# from rest_framework.test import APIClient
#
# from tests.users.test_setup import BaseTest
#
# User = get_user_model()
#
#
# # initialize the APIClient app
# client = Client()
#
#
# class RegisterTest(BaseTest):
#     def test_can_register_user(self):
#         response=self.client.post(self.register_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,200)
#
#     def test_cant_register_user_withshortpassword(self):
#         response=self.client.post(self.register_url,self.user_short_password,format='text/html')
#         self.assertEqual(response.status_code,400)
#
#     def test_cant_register_user_with_unmatching_passwords(self):
#         response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
#         self.assertEqual(response.status_code,400)
#
#     def test_cant_register_user_with_invalid_email(self):
#         response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
#         self.assertEqual(response.status_code,400)
#
#     def test_cant_register_user_with_taken_email(self):
#         self.client.post(self.register_url,self.user,format='text/html')
#         response=self.client.post(self.register_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,400)
#
# class LoginTest(BaseTest):
#     def test_login_success(self):
#         self.client.post(self.register_url,self.user,format='text/html')
#         print(self.user['email'])
#         user=User.objects.filter(email=self.user['email']).first()
#         user.save()
#         response= self.client.post(self.login_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,200)
#
#     def test_cantlogin_with_no_username(self):
#         response= self.client.post(self.login_url,{'password':'passwped','username':''},format='text/html')
#         self.assertEqual(response.status_code,400)
#
#     def test_cantlogin_with_no_password(self):
#         response= self.client.post(self.login_url,{'username':'passwped','password':''},format='text/html')
#         self.assertEqual(response.status_code,400)
#
#
#
# class GetAllUsersTest(TestCase):
#     """ Test module for GET all users API """
#
#     def setUp(self):
#         User.objects.create(
#             username='useranme1', first_name='Name 1', last_name='Surname 1', email='project1@project.com', available=True, auth_provider='email')
#         User.objects.create(
#             username='useranme2', first_name='Name 2', last_name='Surname 2', email='project2@project.com', available=True, auth_provider='email')
#         User.objects.create(
#             username='useranme3', first_name='Name 2', last_name='Surname 3', email='project3@project.com', available=True, auth_provider='email')
#         User.objects.create(
#             username='useranme4', first_name='Name 2', last_name='Surname 4', email='project4@project.com', available=True, auth_provider='email')
#
#     def test_get_all_users(self):
#         response = client.get(reverse('apps.manage_user:registered_users'))
#
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         new_serializer = {
#             "users": serializer.data
#         }
#         self.assertEqual(response.data, new_serializer)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class GetSingleUserTest(TestCase):
#     """ Test module for GET single user API """
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='useranme1', first_name='Name 1', last_name='Surname 1', email='project1@project.com', available=True, auth_provider='email')
#
#     def test_get_valid_single_user(self):
#         response = client.get(
#             reverse('apps.manage_user:user_details', kwargs={'pk': self.user1.pk}))
#         user = User.objects.get(pk=self.user1.pk)
#         serializer = UserSerializer(user)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_invalid_single_user(self):
#         response = client.get(
#             reverse('apps.manage_user:user_details', kwargs={'pk': 10}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class PasswordResetTest(TestCase):
#     """ Test module for Password Reset Request API """
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='useranme11', first_name='Name 11', last_name='Surname 11', email='eelimerdan752@gmail.com', available=True, auth_provider='email')
#
#         self.valid_payload = {
#             'email': 'zackazico@gmail.com',
#
#         }
#         self.invalid_payload = {
#             'email': '',
#         }
#
#     def test_create_valid_password_reset(self):
#         response = client.post(
#             reverse('apps.manage_user:rest_password_reset'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_invalid_password_reset(self):
#         response = client.post(
#             reverse('reset_password'),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class ChangePasswordTest(TestCase):
#     """ Test module for Password Change Request API """
#
#     def setUp(self):
#         user1 = User.objects.create(username='zackazico', first_name='first_name', last_name='last_name', email='example1@gmail.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#         self.valid_payload = {
#             'old_password': 'apple_2001',
#             'new_password1': 'apple_20011',
#             'new_password2': 'apple_20011',
#         }
#         self.invalid_payload = {
#             'old_password': 'apple_2001',
#             'new_password1': 'apple11',
#             'new_password2': 'apple_20011',
#         }
#
#     def test_create_valid_password_change(self):
#         c = Client()
#         c.force_login(self.user1)
#         response = c.post(
#             reverse('changepassword', kwargs={'pk': int(self.user1.pk)}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         u = User.objects.get(username='zackazico')
#         self.assertEqual(u.check_password('apple_20011'), True)
#
#     def test_create_invalid_password_change(self):
#         c = Client()
#         c.force_login(self.user1)
#         response = c.post(
#             reverse('changepassword', kwargs={'pk': int(self.user1.pk)}),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class LogoutTestTest(TestCase):
#     """ Test module for Logout API """
#
#     def setUp(self):
#         user1 = User.objects.create(username='zackazico', first_name='first_name', last_name='last_name', email='example1@gmail.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#     def test_logout(self):
#         c = Client()
#         c.force_login(self.user1)
#         response = c.post(
#             reverse('apps.manage_user:logout'),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class UpdateAvailablityTest(TestCase):
#     """ Test module for UpdateAvailablity API """
#
#     def setUp(self):
#         user1 = User.objects.create(username='zackazico', first_name='first_name', last_name='last_name', email='example1@gmail.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#         self.available_payload = {
#             'available': True
#         }
#
#
#     def test_available(self):
#         c = Client()
#         c.force_login(self.user1)
#         response = c.post(
#             reverse('apps.manage_user:update_profile', kwargs={'pk': int(self.user1.pk)}),
#             {'username': 'zackazico', 'email': 'example1@gmail.com'},
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 405)
#         self.user1.refresh_from_db()
#         self.assertEqual(self.user1.available, True)
#
#
# class FilterUsersByIDTest(TestCase):
#     """ Test module for GET all users API """
#
#     def setUp(self):
#         user1 = User.objects.create(
#             username='useranme1', first_name='Name 1', last_name='Surname 1', email='project1@project.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#     def test_get_all_users(self):
#         response = client.get(reverse('apps.manage_user:search_by_id'))
#
#         users = User.objects.filter(pk=self.user1.pk)
#         serializer = UserSerializer(users, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
#
# class DestroyUserTest(TestCase):
#     """ Test module for Destroy User API """
#
#     def setUp(self):
#         user1 = User.objects.create(username='zackazico', first_name='first_name', last_name='last_name', email='example1@gmail.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user1)
#
#     def test_destroy_user(self):
#         response = self.client.delete(
#             reverse('apps.manage_user:delete_user', kwargs={'pk': int(self.user1.pk)}),
#             content_type='application/json',
#             follow=True
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class PopularUsersTest(TestCase):
#     """ Test module for GET popular users API """
#
#     def setUp(self):
#         new_user1 = User.objects.create(
#             username='username101', first_name='Name 101', last_name='Surname 101', email='project101@project.com', available=True, auth_provider='email')
#         new_user1.set_password('apple_2001')
#         new_user1.save()
#
#         self.user1 = new_user1
#
#     def test_get_popular_users(self):
#         response = client.get(reverse('apps.manage_user:popular_players'))
#
#         users = User.objects.annotate(user__num_likes=Count('profile__num_reviews')).exclude(Q(available=False)).order_by('-profile__num_reviews')[:30]
#         serializer = UserSerializer(users, many=True)
#         # self.assertEqual(sorted(response.data), sorted(serializer.data))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class LatestUsersTest(TestCase):
#     """ Test module for GET popular users API """
#
#     def setUp(self):
#         new_user1 = User.objects.create(
#             username='username101', first_name='Name 101', last_name='Surname 101', email='project101@project.com', available=True, auth_provider='email')
#         new_user1.set_password('apple_2001')
#         new_user1.save()
#
#         self.user1 = new_user1
#
#     def test_get_popular_users(self):
#         response = client.get(reverse('apps.manage_user:latest_players'))
#
#         latest_users = User.objects.all().exclude(Q(available=False)).order_by('-created')[:30]
#         serializer = UserSerializer(latest_users, many=True)
#         self.assertEqual(sorted(response.data), sorted(serializer.data))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# # class RecommendedUsersTest(TestCase):
# #     """ Test module for GET popular users API """
# #
# #     def setUp(self):
# #         new_user1 = User.objects.create(
# #             username='username1011', first_name='Name 1011', last_name='Surname 1011', email='project1011@project.com', available=True, auth_provider='email')
# #         new_user1.set_password('apple_2001')
# #         new_user1.save()
# #
# #         self.user1 = new_user1
# #
# #     def test_get_popular_users(self):
# #         c = Client()
# #         c.force_login(self.user1)
# #
# #         response = c.get(reverse('recommended_players'))
# #
# #         recommended_users = Profile.objects.filter(Q(age__iexact=self.user1.profile.age)
# #         | Q(region__iexact=self.user1.profile.region) | Q(gender__iexact=self.user1.profile.gender) | Q(skill_level__iexact=self.user1.profile.skill_level)).exclude(Q(user__pk__iexact=self.user1.profile.pk) | Q(user__available=False))
# #         serializer = ProfileSerializer(recommended_users, many=True)
# #         self.assertEqual(sorted(response.data), sorted(serializer.data))
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #
#
# class WishListViewSetTest(TestCase):
#     def setUp(self):
#         new_user = User.objects.create(
#             username='username1011', first_name='Name 1011', last_name='Surname 1011', email='project1011@project.com', available=True, auth_provider='email')
#         new_user.set_password('apple_20011')
#         new_user.save()
#
#         new_user1 = User.objects.create(
#             username='username101', first_name='Name 101', last_name='Surname 101', email='project101@project.com', available=True, auth_provider='email')
#         new_user1.favorite_players.add(new_user)
#         new_user1.set_password('apple_2001')
#         new_user1.save()
#
#         self.user1 = new_user1
#
#     def test_all_wishlist_users(self):
#         c = Client()
#         c.force_login(self.user1)
#
#         response = c.get(reverse('apps.manage_user:wishlist'))
#
#         favs = self.user1.favorite_players.all()
#         print(favs)
#         serializer = WishListSerializer(favs, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class AddWishListViewSetTest(TestCase):
#     def setUp(self):
#         new_user = User.objects.create(
#             username='username1011', first_name='Name 1011', last_name='Surname 1011', email='project1011@project.com', available=True, auth_provider='email')
#         new_user.set_password('apple_20011')
#         new_user.save()
#
#         new_user1 = User.objects.create(
#             username='username101', first_name='Name 101', last_name='Surname 101', email='project101@project.com', available=True, auth_provider='email')
#         new_user1.favorite_players.add(new_user)
#         new_user1.set_password('apple_2001')
#         new_user1.save()
#
#         self.user1 = new_user1
#         self.user2 = new_user
#
#     def test_all_wishlist_users(self):
#         c = Client()
#         c.force_login(self.user1)
#
#         response = c.post(reverse('apps.manage_user:add_wishlist'))
#
#         favs = self.user1.favorite_players.add(self.user2)
#         serializer = WishListSerializer(favs, many=True)
#         #self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class FilterUserTest(TestCase):
#     def setUp(self):
#         user1 = User.objects.create(
#             username='useranme1', first_name='Name 1', last_name='Surname 1', email='project1@project.com', available=True, auth_provider='email')
#         user1.set_password('apple_2001')
#         user1.save()
#
#         self.user1 = user1
#
#     def test_get_filter_users(self):
#         response = client.get(reverse('apps.manage_user:filter_user'))
#
#         users = User.objects.filter(Q(username='useranme1') & Q(email='project1@project.com') & Q(first_name='Name 1') & Q(last_name='Surname 1'))
#         serializer = UserSerializer(users, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
