from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsAdmin
from .models import City, Zone
from .serializers import CitySerializer, ZoneSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ZoneViewSet(ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    # TODO: should add permission classes
    # permission_classes = ...


class ZonesOfCityAPIView(APIView):
    def get(self, request, city_id):
        zones = Zone.objects.filter(city=city_id)
        data = [{'id': zone.id, 'name': zone.name, 'city': zone.city.id} for zone in zones]
        return Response(data)
