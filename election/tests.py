from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status

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
DELETE_ZONE_0_ENDPOINT = '/election/cities/0/'
GET_ZONES_OF_ISFAHAN = '/election/cities/0/zones/'
GET_ZONES_OF_TEHRAN = '/election/cities/1/zones/'


class CityTest(TestCase):
    def setUp(self):
        # create cities
        City.objects.create(name='Isfahan', pk=0)
        City.objects.create(name='Tehran', pk=1)
        City.objects.create(name='Shiraz', pk=2)

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
        response = self.client.put(UPDATE_ISFAHAN_ENDPOINT, {'id': 0, 'name': 'Esfahan'},
                                   content_type='application/json')
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


class ZoneTest(TestCase):
    def setUp(self):
        self.isfahan = City.objects.create(name='Isfahan', pk=0)
        tehran = City.objects.create(name='Isfahan', pk=1)

        # isfahan zones
        Zone.objects.create(pk=0, name='z-0', city=isfahan)
        Zone.objects.create(pk=1, name='z-1', city=isfahan)
        Zone.objects.create(pk=2, name='z-2', city=isfahan)

        # tehran zones
        Zone.objects.create(pk=3, name='z-3', city=tehran)
        Zone.objects.create(pk=4, name='z-4', city=tehran)

    def test_get_all_zones(self):
        response = self.client.get(ALL_ZONES_ENDPOINT)

        raw = force_text(response)
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
        response = self.client.put(UPDATE_ZONE_0_ENDPOINT, data={'name': 'updated'})
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
        response = self.client.get(GET_ZONES_OF_ISFAHAN)
        raw = force_text(response)
        excepted_data = [0, 1, 2]
        self.assertJSONEqual(raw, excepted_data)

        response = self.client.get(GET_ZONES_OF_TEHRAN)
        raw = force_text(response)
        excepted_data = [3, 4]
        self.assertJSONEqual(raw, excepted_data)
