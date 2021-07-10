from rest_framework.viewsets import ModelViewSet

from .models import City
from .serializers import CitySerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    # TODO: should add permission classes
    # permission_classes = ...


