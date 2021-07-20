from rest_framework import serializers

from .models import City, Zone, Election, Candidate


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
    candidates = serializers.SerializerMethodField(read_only=True)

    def get_candidates(self, obj):
        return Candidate.objects.filter(election=obj).values_list('id', flat=True)

    class Meta:
        model = Election
        fields = ['id', 'zone_name', 'zone', 'city_name', 'city', 'inspector', 'supervisor', 'candidates', 'status']


class CandidateSerializer(serializers.ModelSerializer):
    vote = serializers.SerializerMethodField(read_only=True)
    election_id = serializers.PrimaryKeyRelatedField(source='election', queryset=Election.objects.all())

    def get_vote(self, obj):
        if obj.election.status == Election.ElectionStatus.ACCEPTED:
            return obj.vote2
        else:
            return None

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'election_id', 'status', 'vote']


class InspectorConfirmVoteSerializer(serializers.ModelSerializer):
    candidate = serializers.IntegerField(source='id')
    vote = serializers.IntegerField(source='vote1')

    class Meta:
        model = Candidate
        fields = ['candidate', 'vote']

    def create(self, validated_data):
        candidate = Candidate.objects.get(pk=validated_data['id'])
        candidate.vote1 = validated_data['vote1']
        candidate.status = Candidate.CandidateStatus.PENDING_FOR_SUPERVISOR
        candidate.save()

        return candidate


class SupervisorConfirmVoteSerializer(serializers.ModelSerializer):
    candidate = serializers.IntegerField(source='id')
    vote = serializers.IntegerField(source='vote2')

    class Meta:
        model = Candidate
        fields = ['candidate', 'vote']

    def create(self, validated_data):
        candidate = Candidate.objects.get(pk=validated_data['id'])
        candidate.vote2 = validated_data['vote2']
        if candidate.vote1 == candidate.vote2:
            candidate.status = Candidate.CandidateStatus.ACCEPTED
        else:
            candidate.status = Candidate.CandidateStatus.REJECTED
        candidate.save()

        return candidate
