from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from account.models import User, Inspector, Supervisor, Admin
from .models import City, Zone, Election, Candidate

import json

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

# City - Zone
GET_ZONES_OF_ISFAHAN = '/election/cities/0/zones/'
GET_ZONES_OF_TEHRAN = '/election/cities/1/zones/'

# Election
ALL_ELECTION_ENDPOINT = '/election/elections/'
GET_ELECTION_0_ENDPOINT = '/election/elections/0/'
CREATE_ELECTION_ENDPOINT = '/election/elections/'
UPDATE_ELECTION_0_ENDPOINT = '/election/elections/0/'
DELETE_ELECTION_0_ENDPOINT = '/election/elections/0/'

# Candidate
ALL_CANDIDATE_ENDPOINT = '/election/candidates/'
GET_CANDIDATE_0_ENDPOINT = '/election/candidates/0/'
CREATE_CANDIDATE_ENDPOINT = '/election/candidates/'
UPDATE_CANDIDATE_0_ENDPOINT = '/election/candidates/0/'
DELETE_CANDIDATE_0_ENDPOINT = '/election/candidates/0/'

# Confirm vote by inspector
INSPECTOR_CONFIRM_VOTE_ENDPOINT = '/election/elections/inspector-confirm-vote/0/'

# Confirm vote by supervisor
SUPERVISOR_CONFIRM_VOTE_ENDPOINT = '/election/elections/supervisor-confirm-vote/0/'


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
        Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        Supervisor.objects.create(user=supervisor)
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
        tehran = City.objects.create(name='Tehran', pk=1)
        City.objects.create(name='Shiraz', pk=2)

        # create test_zone
        zone = Zone.objects.create(pk=0, name='z-0', city=isfahan)
        Zone.objects.create(pk=1, name='z-1', city=isfahan)
        Zone.objects.create(pk=2, name='z-2', city=tehran)

        # create election
        self.election = Election.objects.create(zone=zone)

        self.create_clients()

    def test_all_city(self):
        response = self.client.get(ALL_CITIES_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                'id': 0,
                'name': 'Isfahan',
                'zone_id': [0, 1]
            },
            {
                'id': 1,
                'name': 'Tehran',
                'zone_id': [2]
            },
            {
                'id': 2,
                'name': 'Shiraz',
                'zone_id': []
            }
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_get_isfahan_city(self):
        response = self.client.get(GET_ISFAHAN_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {'id': 0, 'name': 'Isfahan', 'zone_id': [0, 1]}
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
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        Supervisor.objects.create(user=supervisor)
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
        self.isfahan = City.objects.create(name='Isfahan', pk=0)
        tehran = City.objects.create(name='Isfahan', pk=1)

        # isfahan zones
        zone = Zone.objects.create(pk=0, name='z-0', city=self.isfahan)
        Zone.objects.create(pk=1, name='z-1', city=self.isfahan)
        Zone.objects.create(pk=2, name='z-2', city=self.isfahan)

        # tehran zones
        Zone.objects.create(pk=3, name='z-3', city=tehran)
        Zone.objects.create(pk=4, name='z-4', city=tehran)

        # election for test test zone
        self.election = Election.objects.create(pk=0, zone=zone)

        self.create_clients()

    def test_get_all_zones(self):
        response = self.client.get(ALL_ZONES_ENDPOINT)

        raw = force_text(response.content)

        excepted_data = [
            {'id': 0, 'name': 'z-0', 'city_id': 0, 'election_id': 0},
            {'id': 1, 'name': 'z-1', 'city_id': 0, 'election_id': None},
            {'id': 2, 'name': 'z-2', 'city_id': 0, 'election_id': None},
            {'id': 3, 'name': 'z-3', 'city_id': 1, 'election_id': None},
            {'id': 4, 'name': 'z-4', 'city_id': 1, 'election_id': None}
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_create_new_zone(self):
        response = self.client.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_zone(self):
        response = self.client.get(GET_ZONE_3_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {'id': 3, 'name': 'z-3', 'city_id': 1, 'election_id': None}
        self.assertJSONEqual(raw, excepted_data)

    def test_update_zone(self):
        response = self.client.patch(UPDATE_ZONE_0_ENDPOINT, data={'name': 'updated'})
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

    def test_create_zone_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.post(CREATE_ZONE_ENDPOINT, data={'name': 'z-5', 'city_id': 0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_zone_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(GET_ZONE_3_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(GET_ZONE_3_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(GET_ZONE_3_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(GET_ZONE_3_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(GET_ZONE_3_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_zone_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.patch(UPDATE_ZONE_0_ENDPOINT, data={'name': 'updated'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.patch(UPDATE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.patch(UPDATE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.patch(UPDATE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.patch(UPDATE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_zone_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.delete(DELETE_ZONE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_zone_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(ALL_ZONES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(ALL_ZONES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(ALL_ZONES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(ALL_ZONES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(ALL_ZONES_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_zones_of_city_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(GET_ZONES_OF_TEHRAN)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(GET_ZONES_OF_TEHRAN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(GET_ZONES_OF_TEHRAN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(GET_ZONES_OF_TEHRAN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(GET_ZONES_OF_TEHRAN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ElectionViewSetTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        self.inspector = Inspector.objects.create(pk=5, user=inspector)
        self.inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        self.supervisor = Supervisor.objects.create(pk=2, user=supervisor)
        self.supervisor.refresh_from_db()

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
        self.create_clients()

        # create city_0 city_1
        self.city_0 = City.objects.create(name='c-0', pk=0)
        self.city_1 = City.objects.create(name='c-1', pk=1)

        # create zone_0_0 zone_0_1
        self.zone_0_0 = Zone.objects.create(pk=0, name='z-0-0', city=self.city_0)
        self.zone_0_1 = Zone.objects.create(pk=1, name='z-0-1', city=self.city_0)

        # create zone_1_0 zone_1_1
        self.zone_1_0 = Zone.objects.create(pk=2, name='z-1-0', city=self.city_1)
        self.zone_1_1 = Zone.objects.create(pk=3, name='z-1-1', city=self.city_1)

        # create election_0_0 election_0_1 and test_supervisor
        test_user = User.objects.create(username='test_inspector', password='12345')
        test_inspector = Inspector.objects.create(pk=9, user=test_user)

        self.election_0_0 = Election.objects.create(pk=0, zone=self.zone_0_0, inspector=self.inspector)
        self.election_0_1 = Election.objects.create(pk=1, zone=self.zone_0_1, inspector=test_inspector,
                                                    supervisor=self.supervisor)

        # create election_1_0 election_1_1
        self.election_1_0 = Election.objects.create(pk=2, zone=self.zone_1_0)
        self.election_1_1 = Election.objects.create(pk=3, zone=self.zone_1_1)

        # create candidates for election_1_0
        Candidate.objects.create(pk=0, first_name='f0', last_name='l0', election=self.election_1_0)
        Candidate.objects.create(pk=1, first_name='f1', last_name='l1', election=self.election_1_0)
        Candidate.objects.create(pk=2, first_name='f2', last_name='l2', election=self.election_1_0)

        # create candidates for election_0_0
        Candidate.objects.create(pk=3, first_name='f3', last_name='l3', election=self.election_0_0)
        Candidate.objects.create(pk=4, first_name='f4', last_name='l4', election=self.election_0_0)
        Candidate.objects.create(pk=5, first_name='f5', last_name='l5', election=self.election_0_0)
        Candidate.objects.create(pk=6, first_name='f6', last_name='l6', election=self.election_0_0)

    def test_get_all_elections(self):
        response = self.client.get(ALL_ELECTION_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                'id': 0,
                'zone_name': 'z-0-0',
                'zone': 0,
                'city_name': 'c-0',
                'city': 0,
                'inspector': 5,
                'supervisor': None,
                'candidates': [3, 4, 5, 6],
                'status': Election.ElectionStatus.PENDING_FOR_INSPECTOR
            },
            {
                'id': 1,
                'zone_name': 'z-0-1',
                'zone': 1,
                'city_name': 'c-0',
                'city': 0,
                'inspector': 9,
                'supervisor': 2,
                'candidates': [],
                'status': Election.ElectionStatus.PENDING_FOR_INSPECTOR
            },
            {
                'id': 2,
                'zone_name': 'z-1-0',
                'zone': 2,
                'city_name': 'c-1',
                'city': 1,
                'inspector': None,
                'supervisor': None,
                'candidates': [0, 1, 2],
                'status': Election.ElectionStatus.PENDING_FOR_INSPECTOR
            },
            {
                'id': 3,
                'zone_name': 'z-1-1',
                'zone': 3,
                'city_name': 'c-1',
                'city': 1,
                'inspector': None,
                'supervisor': None,
                'candidates': [],
                'status': Election.ElectionStatus.PENDING_FOR_INSPECTOR
            },
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_create_new_election(self):
        city = City.objects.create(name='test city')
        zone = Zone.objects.create(name='test zone', city=city)

        response = self.client.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_election(self):
        response = self.client.get(GET_ELECTION_0_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {
            'id': 0,
            'zone_name': 'z-0-0',
            'zone': 0,
            'city_name': 'c-0',
            'city': 0,
            'inspector': 5,
            'supervisor': None,
            'candidates': [3, 4, 5, 6],
            'status': Election.ElectionStatus.PENDING_FOR_INSPECTOR
        }

        self.assertJSONEqual(raw, excepted_data)

    def test_update_election(self):
        city = City.objects.create(name='new test city')
        zone = Zone.objects.create(name='new test zone', city=city)

        response = self.client.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if Election.objects.filter(zone=zone):
            updated = True
        else:
            updated = False
        self.assertTrue(updated)

    def test_delete_election_0(self):
        response = self.client.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        if Election.objects.filter(zone__name='z-0-0'):
            deleted = False
        else:
            deleted = True
        self.assertTrue(deleted)

    def test_create_election_permission(self):
        city = City.objects.create(name='test city')
        zone = Zone.objects.create(name='test zone', city=city)

        # check for unauthorized - can't
        response = self.client_unauthorized.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.post(CREATE_ELECTION_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_election_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(GET_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(GET_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(GET_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(GET_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(GET_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_election_permission(self):
        city = City.objects.create(name='new test city')
        zone = Zone.objects.create(name='new test zone', city=city)

        # check for unauthorized - can't
        response = self.client_unauthorized.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.patch(UPDATE_ELECTION_0_ENDPOINT, data={'zone': zone.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_election_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.delete(DELETE_ELECTION_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_election_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(ALL_ELECTION_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(ALL_ELECTION_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(ALL_ELECTION_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(ALL_ELECTION_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(ALL_ELECTION_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CandidateViewSetTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        Supervisor.objects.create(user=supervisor)
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
        # create city_0 city_1
        self.city_0 = City.objects.create(name='c-0', pk=0)

        # create zone_0_0 zone_0_1
        self.zone_0_0 = Zone.objects.create(pk=0, name='z-0-0', city=self.city_0)
        self.zone_0_1 = Zone.objects.create(pk=1, name='z-0-1', city=self.city_0)

        # create election_0_0 election_0_1
        self.election_0_0 = Election.objects.create(pk=0, zone=self.zone_0_0)
        self.election_0_1 = Election.objects.create(pk=1, zone=self.zone_0_1)

        # create candidates for election_0_0
        Candidate.objects.create(pk=0, first_name='f0', last_name='l0', election=self.election_0_0)
        Candidate.objects.create(pk=1, first_name='f1', last_name='l1', election=self.election_0_0)
        Candidate.objects.create(pk=2, first_name='f2', last_name='l2', election=self.election_0_0)

        # create candidates for election_0_1
        Candidate.objects.create(pk=3, first_name='f3', last_name='l3', election=self.election_0_1)
        Candidate.objects.create(pk=4, first_name='f4', last_name='l4', election=self.election_0_1)

        self.create_clients()

    def test_get_all_candidate(self):
        response = self.client.get(ALL_CANDIDATE_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = [
            {
                'id': 0,
                'first_name': 'f0',
                'last_name': 'l0',
                'election_id': self.election_0_0.id,
                'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
                'vote': None
            },
            {
                'id': 1,
                'first_name': 'f1',
                'last_name': 'l1',
                'election_id': self.election_0_0.id,
                'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
                'vote': None
            },
            {
                'id': 2,
                'first_name': 'f2',
                'last_name': 'l2',
                'election_id': self.election_0_0.id,
                'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
                'vote': None
            },
            {
                'id': 3,
                'first_name': 'f3',
                'last_name': 'l3',
                'election_id': self.election_0_1.id,
                'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
                'vote': None
            },
            {
                'id': 4,
                'first_name': 'f4',
                'last_name': 'l4',
                'election_id': self.election_0_1.id,
                'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
                'vote': None
            }
        ]
        self.assertJSONEqual(raw, excepted_data)

    def test_create_new_candidate(self):
        city = City.objects.create(name='test city')
        zone = Zone.objects.create(name='test zone', city=city)
        election = Election.objects.create(zone=zone)

        data = {
            'first_name': 'test first_name',
            'last_name': 'test last_name',
            'election_id': election.id,
            'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR
        }

        response = self.client.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_candidate(self):
        response = self.client.get(GET_CANDIDATE_0_ENDPOINT)

        raw = force_text(response.content)
        excepted_data = {
            'id': 0,
            'first_name': 'f0',
            'last_name': 'l0',
            'election_id': self.election_0_0.id,
            'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR,
            'vote': None
        }

        self.assertJSONEqual(raw, excepted_data)

    def test_update_candidate(self):
        response = self.client.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if Candidate.objects.filter(first_name='new first_name'):
            updated = True
        else:
            updated = False
        self.assertTrue(updated)

    def test_delete_candidate_0(self):
        response = self.client.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        if Candidate.objects.filter(pk=0):
            deleted = False
        else:
            deleted = True
        self.assertTrue(deleted)

    def test_create_candidate_permission(self):
        city = City.objects.create(name='test city')
        zone = Zone.objects.create(name='test zone', city=city)
        election = Election.objects.create(zone=zone)

        data = {
            'first_name': 'test first_name',
            'last_name': 'test last_name',
            'election_id': election.id,
            'status': Candidate.CandidateStatus.PENDING_FOR_INSPECTOR
        }

        # check for unauthorized - can't
        response = self.client_unauthorized.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.post(CREATE_CANDIDATE_ENDPOINT, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_candidate_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(GET_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(GET_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(GET_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(GET_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(GET_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_candidate_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.patch(UPDATE_CANDIDATE_0_ENDPOINT, data={'first_name': 'new first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_candidate_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can
        response = self.client_admin.delete(DELETE_CANDIDATE_0_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_candidate_permission(self):
        # check for unauthorized - can't
        response = self.client_unauthorized.get(ALL_CANDIDATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can
        response = self.client_visitor.get(ALL_CANDIDATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for inspector - can
        response = self.client_inspector.get(ALL_CANDIDATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for supervisor - can
        response = self.client_supervisor.get(ALL_CANDIDATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check for admin - can
        response = self.client_admin.get(ALL_CANDIDATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InspectorConfirmVoteTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector_of_election
        inspector = User.objects.create(username='inspector', password='12345')
        self.inspector_of_election = Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector_of_election = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector_of_election.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector_of_another_election
        inspector = User.objects.create(username='inspector_2', password='12345')
        self.inspector_of_another_election = Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector_of_another_election = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector_of_another_election.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        self.supervisor = Supervisor.objects.create(user=supervisor)
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

        # create self.client_unauthorized
        self.client_unauthorized = APIClient()

    def setUp(self):
        self.create_clients()
        self.client = self.client_inspector_of_election

        # create city_0
        self.city_0 = City.objects.create(name='c-0', pk=0)

        # create zone_0_0
        self.zone_0_0 = Zone.objects.create(pk=0, name='z-0-0', city=self.city_0)

        # create election_0_0
        self.election_0_0 = Election.objects.create(pk=0, zone=self.zone_0_0, inspector=self.inspector_of_election,
                                                    supervisor=self.supervisor)

        # create candidates for election_0_0
        self.candidate_0 = Candidate.objects.create(pk=3, first_name='f3', last_name='l3', election=self.election_0_0)
        self.candidate_1 = Candidate.objects.create(pk=4, first_name='f4', last_name='l4', election=self.election_0_0)
        self.candidate_2 = Candidate.objects.create(pk=5, first_name='f5', last_name='l5', election=self.election_0_0)
        self.candidate_3 = Candidate.objects.create(pk=6, first_name='f6', last_name='l6', election=self.election_0_0)

    def test_confirm_vote(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]
        response = self.client.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check vote1:
        self.candidate_0.refresh_from_db()
        self.assertEqual(self.candidate_0.vote1, 10)

        self.candidate_1.refresh_from_db()
        self.assertEqual(self.candidate_1.vote1, 20)

        self.candidate_2.refresh_from_db()
        self.assertEqual(self.candidate_2.vote1, 30)

        self.candidate_3.refresh_from_db()
        self.assertEqual(self.candidate_3.vote1, 50)

    def test_confirm_vote_permission_inspector(self):  # only inspector of election can.
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]

        # check for unauthorized - can't
        response = self.client_unauthorized.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                 content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector of this election - can
        response = self.client_inspector_of_election.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                          content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check for inspector of another election - can't
        response = self.client_inspector_of_another_election.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                                  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor - can't
        response = self.client_supervisor.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can't
        response = self.client_admin.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                          content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_vote_permission_election_status(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]

        # check for inspector of this election but election status is not valid - can't
        election_status = Election.ElectionStatus
        for s in (election_status.PENDING_FOR_SUPERVISOR, election_status.REJECTED, election_status.ACCEPTED):
            self.election_0_0.status = s
            self.election_0_0.save()

            response = self.client_inspector_of_election.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                              content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SupervisorConfirmVoteTest(TestCase):
    def create_clients(self):
        # create self.client_visitor
        visitor = User.objects.create_user(username='visitor', password='12345')

        self.client_visitor = APIClient()
        token = Token.objects.create(user=visitor)
        token.save()
        self.client_visitor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        self.inspector = Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor_of_election
        supervisor = User.objects.create(username='supervisor', password='12345')
        self.supervisor_of_election = Supervisor.objects.create(user=supervisor)
        supervisor.refresh_from_db()

        self.client_supervisor_of_election = APIClient()
        token = Token.objects.create(user=supervisor)
        token.save()
        self.client_supervisor_of_election.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor_of_another_election
        supervisor = User.objects.create(username='supervisor_2', password='12345')
        self.supervisor_of_another_election = Supervisor.objects.create(user=supervisor)
        supervisor.refresh_from_db()

        self.client_supervisor_of_another_election = APIClient()
        token = Token.objects.create(user=supervisor)
        token.save()
        self.client_supervisor_of_another_election.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_admin = self.client
        admin = User.objects.create(username='admin', password='12345')
        Admin.objects.create(user=admin)
        admin.refresh_from_db()

        self.client_admin = APIClient()
        token = Token.objects.create(user=admin)
        token.save()
        self.client_admin.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_unauthorized
        self.client_unauthorized = APIClient()

    def setUp(self):
        self.create_clients()
        self.client = self.client_supervisor_of_election

        # create city_0
        self.city_0 = City.objects.create(name='c-0', pk=0)

        # create zone_0_0
        self.zone_0_0 = Zone.objects.create(pk=0, name='z-0-0', city=self.city_0)

        # create election_0_0
        self.election_0_0 = Election.objects.create(pk=0, zone=self.zone_0_0, inspector=self.inspector,
                                                    supervisor=self.supervisor_of_election,
                                                    status=Election.ElectionStatus.PENDING_FOR_SUPERVISOR)

        # create candidates for election_0_0
        self.candidate_0 = Candidate.objects.create(pk=3, first_name='f3', last_name='l3', election=self.election_0_0,
                                                    vote1=10)
        self.candidate_1 = Candidate.objects.create(pk=4, first_name='f4', last_name='l4', election=self.election_0_0,
                                                    vote1=20)
        self.candidate_2 = Candidate.objects.create(pk=5, first_name='f5', last_name='l5', election=self.election_0_0,
                                                    vote1=30)
        self.candidate_3 = Candidate.objects.create(pk=6, first_name='f6', last_name='l6', election=self.election_0_0,
                                                    vote1=50)

    def test_confirm_vote(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]
        response = self.client.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check vote1:
        self.candidate_0.refresh_from_db()
        self.assertEqual(self.candidate_0.vote2, 10)

        self.candidate_1.refresh_from_db()
        self.assertEqual(self.candidate_1.vote2, 20)

        self.candidate_2.refresh_from_db()
        self.assertEqual(self.candidate_2.vote2, 30)

        self.candidate_3.refresh_from_db()
        self.assertEqual(self.candidate_3.vote2, 50)

    def test_confirm_vote_permission_supervisor(self):  # only supervisor of election can.
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]

        # check for unauthorized - can't
        response = self.client_unauthorized.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                 content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check for visitor - can't
        response = self.client_visitor.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for inspector - can't
        response = self.client_inspector.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for supervisor_of_election - can
        response = self.client_supervisor_of_election.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check for supervisor_of_another_election - can't
        response = self.client_supervisor_of_another_election.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # check for admin - can't
        response = self.client_admin.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                          content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_vote_permission_election_status(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]

        # check for supervisor of this election but election status is not valid - can't
        election_status = Election.ElectionStatus
        for s in (election_status.PENDING_FOR_INSPECTOR, election_status.REJECTED, election_status.ACCEPTED):
            self.election_0_0.status = s
            self.election_0_0.save()

            response = self.client.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data),
                                        content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CandidateStatusTest(TestCase):
    def create_clients(self):
        # create self.client_inspector
        inspector = User.objects.create(username='inspector', password='12345')
        self.inspector = Inspector.objects.create(user=inspector)
        inspector.refresh_from_db()

        self.client_inspector = APIClient()
        token = Token.objects.create(user=inspector)
        token.save()
        self.client_inspector.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create self.client_supervisor
        supervisor = User.objects.create(username='supervisor', password='12345')
        self.supervisor = Supervisor.objects.create(user=supervisor)
        supervisor.refresh_from_db()

        self.client_supervisor = APIClient()
        token = Token.objects.create(user=supervisor)
        token.save()
        self.client_supervisor.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def setUp(self):
        self.create_clients()

        # create city
        self.city = City.objects.create(name='c-o', pk=0)

        # create zone
        self.zone = Zone.objects.create(pk=0, name='z-0', city=self.city)

        # create election
        self.election = Election.objects.create(pk=0, zone=self.zone, inspector=self.inspector,
                                                supervisor=self.supervisor)

        # create candidates for election_0_0
        self.candidate_0 = Candidate.objects.create(pk=3, first_name='f3', last_name='l3', election=self.election)
        self.candidate_1 = Candidate.objects.create(pk=4, first_name='f4', last_name='l4', election=self.election)
        self.candidate_2 = Candidate.objects.create(pk=5, first_name='f5', last_name='l5', election=self.election)
        self.candidate_3 = Candidate.objects.create(pk=6, first_name='f6', last_name='l6', election=self.election)

    def test_initial_candidates_status(self):  # candidates status should be Pending For Inspector
        candidates = Candidate.objects.all()
        for candidate in candidates:
            self.assertEqual(candidate.status, Candidate.CandidateStatus.PENDING_FOR_INSPECTOR)

    def test_candidates_status_after_inspector_submit_vote(self):  # candidates status should be Pending For Supervisor
        self.inspector_submit_vote()

        candidates = Candidate.objects.all()
        for candidate in candidates:
            self.assertEqual(candidate.status, Candidate.CandidateStatus.PENDING_FOR_SUPERVISOR)

    def test_candidates_status_after_supervisor_submit_correct_vote(self):  # candidates status should be Accepted

        self.inspector_submit_vote()
        self.supervisor_submit_correct_vote()

        candidates = Candidate.objects.all()
        for candidate in candidates:
            self.assertEqual(candidate.status, Candidate.CandidateStatus.ACCEPTED)

    def test_candidates_status_after_supervisor_submit_incorrect_vote(self):
        # candidate status should be Accepted except candidate(3) and  candidate(5) Rejected

        self.inspector_submit_vote()
        self.supervisor_submit_incorrect_vote()

        candidates = Candidate.objects.all()
        for candidate in candidates:
            if candidate.id in [3, 5]:
                self.assertEqual(candidate.status, Candidate.CandidateStatus.REJECTED)
            else:
                self.assertEqual(candidate.status, Candidate.CandidateStatus.ACCEPTED)

    def inspector_submit_vote(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]
        self.client_inspector.post(INSPECTOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data), content_type='application/json')

    def supervisor_submit_correct_vote(self):
        data = [
            {'candidate': 3, 'vote': 10},
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 30},
            {'candidate': 6, 'vote': 50},
        ]
        self.client_supervisor.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data), content_type='application/json')

    def supervisor_submit_incorrect_vote(self):
        # candidate(3) and  candidate(5) have incorrect vote
        data = [
            {'candidate': 4, 'vote': 20},
            {'candidate': 5, 'vote': 21},
            {'candidate': 3, 'vote': 9},
            {'candidate': 6, 'vote': 50},
        ]
        self.client_supervisor.post(SUPERVISOR_CONFIRM_VOTE_ENDPOINT, json.dumps(data), content_type='application/json')
