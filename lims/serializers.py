from django.contrib.auth.models import User, Group, Permission
from .models import Workflow, Processor, Task
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ['name', 'input_path', 'interval']

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = ['name', 'description', 'file_type']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['workflow', 'input_file', 'start_time', 'status']