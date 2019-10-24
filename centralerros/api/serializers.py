from rest_framework import serializers

from api.models import User, Group, Environment, Agent, Level, Event


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'last_login', 'group']


class EnvironmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ['id', 'name']


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'address', 'status', 'environment', 'version']


class LevelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']


class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'level', 'data', 'agent', 'shelved', 'date']
