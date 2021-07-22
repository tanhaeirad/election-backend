from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status

from .models import User, Inspector, Supervisor, Admin
from election.models import City, Zone, Election

# Define CONSTANTS
LOGIN_ENDPOINT = '/account/login/'
REGISTER_ENDPOINT = '/account/register/'
GET_ALL_USERS_ENDPOINT = '/account/users/'


class AccountTest(TestCase):
    def setUp(self):
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
        # create user1 visitor
        user1 = User.objects.create_user(username='user1', password='123')

        # create user2 inspector
        user2 = User.objects.create_user(username='user2', password='123')
        Inspector.objects.create(user=user2, election=self.election)

        # create user3 supervisor
        user3 = User.objects.create_user(username='user3', password='123')
        Supervisor.objects.create(user=user3, election=self.election)

        # create user4 admin
        user4 = User.objects.create_user(username='user4', password='123')
        Admin.objects.create(user=user4)

        response = self.client.get(GET_ALL_USERS_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                'username': 'user1',
                'kind': 'Visitor'
            },
            {
                'username': 'user2',
                'kind': 'Inspector'
            },
            {
                'username': 'user3',
                'kind': 'Supervisor'
            },
            {
                'username': 'user4',
                'kind': 'Admin'
            }
        ]
        self.assertJSONEqual(raw, excepted_data)
