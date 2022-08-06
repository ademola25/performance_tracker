# from django.test import TestCase, override_settings
# from django.test import Client

# from accounts.models import User



# class ObjectsCreation(object):

#     def setUp(self):
#         self.client = Client()

#         self.super_user = User.objects.create(name="john doe",
#                                                   role="hr",
#                                                   email='johndoe@admin.com',
#                                                   staff_id='UBA01234',
#                                                   admin=True,
#                                                   staff=True,
#                                                   is_active=True)

#         self.super_user.set_password('password')
#         self.super_user.save()
#         self.user = User.objects.create(name="jane doe",
#                                                   role="hr",
#                                                   email='janedoe@admin.com',
#                                                   staff_id='UBA1234',
#                                                   admin=True,
#                                                   staff=True,
#                                                   is_active=True)
#         self.user.set_password('password')
#         self.user.save()
#         with self.settings(AXES_ENABLED=False):
#             self.client.login(
#                 email='johndoe@admin.com', password='password')





# class TestHomePage(ObjectsCreation, TestCase):

#     def test_anonymous_home_page(self):
#         self.client.logout()
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)


#     def test_invalid_login_home_page(self):
#         self.client.logout()
#         self.client.login(
#             email='mp@micropyramid.com', password='mp')
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)


#     def test_valid_login_home_page(self):
#         self.client.login(
#             email="oketofoke@gmail.com",
#             password='password')
#         response = self.client.get('/', follow=True)
#         self.assertEqual(response.status_code, 200)



# class LoginViewTestCase(ObjectsCreation, TestCase):
#     def test_login_post(self):
#         self.client.logout()
#         data = {"email": "johndoe@admin.com", "password": "password"}
#         response = self.client.post('/', data)
#         self.assertEqual(response.status_code, 302)

#     def test_login_get_request(self):
#         data = {"email": "johndoe@admin.com", "password": "password"}
#         response = self.client.post('/', data)
#         self.assertEqual(response.status_code, 302)

#     def test_login_post_invalid(self):
#         self.client.logout()
#         data = {"email": "xxx@admin.com", "password": "test123"}
#         response = self.client.post('/', data)

#         self.assertEqual(response.status_code, 302)

#     def test_login_inactive(self):
#         self.client.logout()
#         data = {
#             "email": "johndoe@admin.com",
#             "password": "password",
#             'is_active': False
#         }
#         response = self.client.post('/', data)
#         self.assertEqual(response.status_code, 302)

#     def test_login_invalid(self):
#         self.client.logout()
#         data = {"email": "abc@abc.com", "password": "123"}
#         response = self.client.post('/', data)
#         self.assertEqual(response.status_code, 302)

#     def test_logout(self):
#         self.client = Client()
#         self.client.login(email="johndoe@admin.com",
#                           password="password")
#         response = self.client.get("/logout")
#         self.assertEqual(response.status_code, 302)
