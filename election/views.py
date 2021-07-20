from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsAdmin, IsInspector, IsSupervisor
from .models import City, Zone, Election, Candidate
from .permissions import CanInspectorConfirmVote, CanSupervisorConfirmVote
from .serializers import CitySerializer, ZoneSerializer, ElectionSerializer, CandidateSerializer, \
    InspectorConfirmVoteSerializer, SupervisorConfirmVoteSerializer

from rest_framework.generics import ListAPIView, ListCreateAPIView


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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ZonesOfCityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city_id):
        zones = Zone.objects.filter(city=city_id)
        data = [{'id': zone.id, 'name': zone.name, 'city': zone.city.id} for zone in zones]
        return Response(data, status=status.HTTP_200_OK)


class ElectionViewSet(ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CandidateViewSet(ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class InspectorConfirmVoteAPIView(APIView):
    permission_classes = [CanInspectorConfirmVote, IsInspector]

    def post(self, request, election_id):
        election = Election.objects.get(pk=election_id)

        # check obj permissions
        self.check_object_permissions(request, election)

        inspector_confirm_vote_serializer = InspectorConfirmVoteSerializer(data=request.data, many=True)
        if inspector_confirm_vote_serializer.is_valid():
            inspector_confirm_vote_serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SupervisorConfirmVoteAPIView(APIView):
    pass
