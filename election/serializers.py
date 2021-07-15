from rest_framework import serializers

from .models import City, Zone, Election


class CitySerializer(serializers.ModelSerializer):
    zone_id = serializers.SerializerMethodField(read_only=True)

    def get_zone_id(self, obj):
        return Zone.objects.filter(city=obj).values_list('id', flat=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'zone_id']


class ZoneSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(source='city', queryset=City.objects.all())
    election_id = serializers.SerializerMethodField(method_name='get_election_id', read_only=True)

    def get_election_id(self, obj):
        election_id = None
        try:
            election_id = Election.objects.get(zone=obj).id
        except Election.DoesNotExist:
            election_id = None
        finally:
            return election_id

    class Meta:
        model = Zone
        fields = ['id', 'name', 'city_id', 'election_id']


class ElectionSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(max_length=255, source='zone.name', read_only=True)
    city_name = serializers.CharField(max_length=255, source='zone.city.name', read_only=True)
    city = serializers.IntegerField(source='zone.city.pk', read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'zone_name', 'zone', 'city_name', 'city', 'status']
