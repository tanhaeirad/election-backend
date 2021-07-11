from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from account.models import User, Inspector, Supervisor, Admin
from .models import City, Zone

# Define CONSTANTS

# City
ALL_CITIES_ENDPOINT = '/election/cities/'
GET_ISFAHAN_ENDPOINT = '/election/cities/0/'
CREATE_TABRIZ_CITY_ENDPOINT = '/election/cities/'
UPDATE_ISFAHAN_ENDPOINT = '/election/cities/0/'
DELETE_ISFAHAN_ENDPOINT = '/election/cities/0/'

# Zone
ALL_ZONES_ENDPOINT = '/election/zones/'
GET_ZONE_3_ENDPOINT = '/election/zones/3/'
CREATE_ZONE_ENDPOINT = '/election/zones/'
UPDATE_ZONE_0_ENDPOINT = '/election/zones/0/'
DELETE_ZONE_0_ENDPOINT = '/election/zones/0/'
GET_ZONES_OF_ISFAHAN = '/election/cities/0/zones/'
GET_ZONES_OF_TEHRAN = '/election/cities/1/zones/'


class CityTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        Inspector.objects.create(user=inspector, zone=self.test_zone)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        Supervisor.objects.create(user=supervisor, zone=self.test_zone)
        supervisor.refresh_from_db()

        self.client_supervisor = APIClient()
        token = Token.objects.create(user=supervisor)
        token.save()
        self.client_supervisor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_admin = self.client
        admin = User.objects.create(username='admin', password='12345')
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
        # create cities
        isfahan = City.objects.create(name='Isfahan', pk=0)
        City.objects.create(name='Tehran', pk=1)
        City.objects.create(name='Shiraz', pk=2)

        # create test_zone
        self.test_zone = Zone.objects.create(pk=0, name='z-0', city=isfahan)

        self.create_clients()

    def test_all_city(self):
        response = self.client.get(ALL_CITIES_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                'id': 0,
                'name': 'Isfahan'
            },
            {
                'id': 1,
                'name': 'Tehran',
            },
            {
                'id': 2,
                'name': 'Shiraz'
            }
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_get_isfahan_city(self):
        response = self.client.get(GET_ISFAHAN_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {'id': 0, 'name': 'Isfahan'}
        self.assertJSONEqual(raw, excepted_data)

    def test_create_tabriz_city(self):
        response = self.client.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'Tabriz'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_isfahan_city(self):
        response = self.client.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'Esfahan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if City.objects.filter(name='Esfahan') and not City.objects.filter(name='Isfahan'):
            updated = True
        else:
            updated = False

        self.assertTrue(updated)

    def test_delete_isfahan_city(self):
        self.client.delete(DELETE_ISFAHAN_ENDPOINT)
        if City.objects.filter(name='Isfahan'):
            deleted = False
        else:
            deleted = True

        self.assertTrue(deleted)

    def test_create_city_permissions(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'tabriz'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'tabriz'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'tabriz'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'tabriz'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.post(CREATE_TABRIZ_CITY_ENDPOINT, data={'name': 'tabriz'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_city_permissions(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(GET_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(GET_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(GET_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(GET_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(GET_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_city_permissions(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'new city'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'new city'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'new city'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'new city'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.patch(UPDATE_ISFAHAN_ENDPOINT, data={'id': 0, 'name': 'new city'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_city_permissions(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.delete(DELETE_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.delete(DELETE_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.delete(DELETE_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.delete(DELETE_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.delete(DELETE_ISFAHAN_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_city_permissions(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(ALL_CITIES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(ALL_CITIES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(ALL_CITIES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(ALL_CITIES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(ALL_CITIES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class ZoneTest(TestCase):
    def setUp(self):
        self.isfahan = City.objects.create(name='Isfahan', pk=0)
        tehran = City.objects.create(name='Isfahan', pk=1)

        # isfahan zones
        Zone.objects.create(pk=0, name='z-0', city=self.isfahan)
        Zone.objects.create(pk=1, name='z-1', city=self.isfahan)
        Zone.objects.create(pk=2, name='z-2', city=self.isfahan)

        # tehran zones
        Zone.objects.create(pk=3, name='z-3', city=tehran)
        Zone.objects.create(pk=4, name='z-4', city=tehran)

    def test_get_all_zones(self):
        response = self.client.get(ALL_ZONES_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {'id': 0, 'name': 'z-0', 'city': 0},
            {'id': 1, 'name': 'z-1', 'city': 0},
            {'id': 2, 'name': 'z-2', 'city': 0},
            {'id': 3, 'name': 'z-3', 'city': 1},
            {'id': 4, 'name': 'z-4', 'city': 1}
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_create_new_zone(self):
        response = self.client.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city': self.isfahan.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(GET_ZONE_3_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {'id': 3, 'name': 'z-3', 'city': 1}
        self.assertJSONEqual(raw, excepted_data)

    def test_update_zone(self):
        response = self.client.patch(UPDATE_ZONE_0_ENDPOINT, data={'name': 'updated'}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if Zone.objects.filter(name='updated'):
            updated = True
        else:
            updated = False
        self.assertTrue(updated)

    def test_delete_zone_0(self):
        response = self.client.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        if Zone.objects.filter(name='z-0'):
            deleted = False
        else:
            deleted = True
        self.assertTrue(deleted)

    def test_get_zones_of_isfahan_and_tehran(self):
        response = self.client.get(GET_ZONES_OF_TEHRAN)
        raw = force_text(response.content)
        excepted_data = [
            {
                "id": 3,
                "name": "z-3",
                "city": 1
            },
            {
                "id": 4,
                "name": "z-4",
                "city": 1
            }
        ]
        self.assertJSONEqual(raw, excepted_data)

        response = self.client.get(GET_ZONES_OF_ISFAHAN)
        raw = force_text(response.content)
        excepted_data = [
            {
                "id": 0,
                "name": "z-0",
                "city": 0
            },
            {
                "id": 1,
                "name": "z-1",
                "city": 0
            },
            {
                "id": 2,
                "name": "z-2",
                "city": 0
            }
        ]
        self.assertJSONEqual(raw, excepted_data)
