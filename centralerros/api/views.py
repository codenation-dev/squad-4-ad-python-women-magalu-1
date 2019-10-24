from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    GroupModelSerializer,
    UserModelSerializer,
    EnvironmentModelSerializer,
    AgentModelSerializer,
    LevelModelSerializer,
    EventModelSerializer
)

from api.models import User, Group, Environment, Agent, Level, Event

class UserApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class GroupListOnlyAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        

class EnvironmentListOnlyAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Environment.objects.all()
    serializer_class = EnvironmentModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AgentApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer


class LevelListOnlyAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Level.objects.all()
    serializer_class = LevelModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventModelSerializer