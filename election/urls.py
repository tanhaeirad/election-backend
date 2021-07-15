from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CityViewSet, ZoneViewSet, ZonesOfCityAPIView, ElectionViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'zones', ZoneViewSet, basename='zone')
router.register(r'elections', ElectionViewSet, basename='election')

urlpatterns = [
    *router.urls,
    path('cities/<int:city_id>/zones/', view=ZonesOfCityAPIView.as_view(), name='zones-of-city'),
]
