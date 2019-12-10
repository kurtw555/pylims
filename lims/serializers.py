from django.contrib.auth.models import User, Group, Permission

from lims.models import Task, Workflow
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'workflow', 'status', 'date']


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workflow
        fields = ['name', 'processor', 'inputPath', 'outputPath', 'frequency']
