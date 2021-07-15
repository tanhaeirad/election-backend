from rest_framework import serializers

from .models import City, Zone, Election


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class ElectionSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(max_length=255, source='zone.name', read_only=True)
    city_name = serializers.CharField(max_length=255, source='zone.city.name', read_only=True)
    city = serializers.IntegerField(source='zone.city.pk', read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'zone_name', 'zone', 'city_name', 'city', 'status']

