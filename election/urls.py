from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CityViewSet, ZoneViewSet, ZonesOfCityAPIView, ElectionViewSet, CandidateViewSet, \
    InspectorConfirmVoteAPIView, SupervisorConfirmVoteAPIView,ResetAllElectionsAPIView

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'zones', ZoneViewSet, basename='zone')
router.register(r'elections', ElectionViewSet, basename='election')
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = [
    *router.urls,
    path('cities/<int:city_id>/zones/', view=ZonesOfCityAPIView.as_view(), name='zones-of-city'),
    path('elections/inspector-confirm-vote/<int:election_id>/', view=InspectorConfirmVoteAPIView.as_view(),
         name='inspector-confirm-votes'),
    path('elections/supervisor-confirm-vote/<int:election_id>/', view=SupervisorConfirmVoteAPIView.as_view(),
         name='supervisor-confirm-votes'),
    path('reset/', view=ResetAllElectionsAPIView.as_view(), name='reset-all')
]
