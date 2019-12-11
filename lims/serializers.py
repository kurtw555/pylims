from django.contrib.auth.models import User, Group, Permission
from .models import Workflow, Processor, Task
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

class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workflow
        fields = ['processor', 'input_path', 'interval']

class ProcessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Processor
        fields = ['name', 'description', 'file_type']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['workflow', 'input_file', 'start_time', 'status']