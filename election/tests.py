from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework import status

from .models import City

# Define CONSTANTS

# City
ALL_CITIES_ENDPOINT = '/election/cities/'
GET_ISFAHAN_ENDPOINT = '/election/cities/0/'
CREATE_TABRIZ_CITY_ENDPOINT = '/election/cities/'
UPDATE_ISFAHAN_ENDPOINT = '/election/cities/0/'
DELETE_ISFAHAN_ENDPOINT = '/election/cities/0/'


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
