from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import User, Inspector, Supervisor, Admin
from election.models import City, Zone, Election

# Define CONSTANTS
LOGIN_ENDPOINT = '/account/login/'
REGISTER_ENDPOINT = '/account/register/'
GET_ALL_USERS_ENDPOINT = '/account/users/'
GET_CURRENT_USER_ENDPOINT = '/account/users/me/'
RETRIEVE_USER_ENDPOINT = '/account/users/2/'


class AccountTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(id=0, username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(id=1, username='inspector', password='12345')
        Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(id=2, username='supervisor', password='12345')
        Supervisor.objects.create(user=supervisor)
        supervisor.refresh_from_db()

        self.client_supervisor = APIClient()
        token = Token.objects.create(user=supervisor)
        token.save()
        self.client_supervisor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_admin = self.client
        admin = User.objects.create(id=3, username='admin', password='12345')
        Admin.objects.create(user=admin)
        admin.refresh_from_db()

        self.client_admin = APIClient()
        token = Token.objects.create(user=admin)
        token.save()
        self.client_admin.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.client = self.client_admin

        # create self.client_unauthorized
        self.client_unauthorized = APIClient()

    def setUp(self):
        self.create_clients()

        city = City.objects.create(name='test city')
        zone = Zone.objects.create(name='test zone', city=city)
        self.election = Election.objects.create(zone=zone)

    def test_login(self):
        User.objects.create_user('test_user', 'something@gmail.com', '123')

        # good login
        data = {'username': 'test_user', 'password': '123'}
        response = self.client.post(LOGIN_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # bad login
        data = {'username': 'admin', 'password': '321'}
        response = self.client.post(LOGIN_ENDPOINT, data=data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        # good register
        data = {'username': 'user1', 'password': '123', 'password2': '123'}
        response = self.client.post(REGISTER_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # bad register - username is exist
        data = {'username': 'user1', 'password': '321', 'password2': '321'}
        response = self.client.post(REGISTER_ENDPOINT, data=data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

        # bad register - password and password2 not the same
        data = {'username': 'user2', 'password': '123', 'password2': '321'}
        response = self.client.post(REGISTER_ENDPOINT, data=data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_user(self):
        response = self.client.get(GET_ALL_USERS_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                "id": 0,
                "username": "visitor",
                "kind": User.UserKind.VISITOR
            },
            {
                "id": 1,
                "username": "inspector",
                "kind": User.UserKind.INSPECTOR
            },
            {
                "id": 2,
                "username": "supervisor",
                "kind": User.UserKind.SUPERVISOR
            },
            {
                "id": 3,
                "username": "admin",
                "kind": User.UserKind.ADMIN
            },

        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_get_current_user(self):
        # for visitor client
        response = self.client_visitor.get(GET_CURRENT_USER_ENDPOINT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        raw = force_text(response.content)
        excepted_data = {
            "id": 0,
            "username": "visitor",
            "kind": User.UserKind.VISITOR
        }
        self.assertJSONEqual(raw, excepted_data)

        # for inspector client
        response = self.client_inspector.get(GET_CURRENT_USER_ENDPOINT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        raw = force_text(response.content)
        excepted_data = {
            "id": 1,
            "username": "inspector",
            "kind": User.UserKind.INSPECTOR
        }
        self.assertJSONEqual(raw, excepted_data)

        # for supervisor client
        response = self.client_supervisor.get(GET_CURRENT_USER_ENDPOINT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        raw = force_text(response.content)
        excepted_data = {
            "id": 2,
            "username": "supervisor",
            "kind": User.UserKind.SUPERVISOR
        }
        self.assertJSONEqual(raw, excepted_data)

        # for admin client
        response = self.client_admin.get(GET_CURRENT_USER_ENDPOINT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        raw = force_text(response.content)
        excepted_data = {
            "id": 3,
            "username": "admin",
            "kind": User.UserKind.ADMIN
        }
        self.assertJSONEqual(raw, excepted_data)

        # for unauthorized client
        response = self.client_unauthorized.get(GET_CURRENT_USER_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        response = self.client.get(RETRIEVE_USER_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        raw = force_text(response.content)
        excepted_data = {
            "id": 2,
            "username": "supervisor",
            "kind": User.UserKind.SUPERVISOR
        }

        self.assertJSONEqual(raw, excepted_data)
