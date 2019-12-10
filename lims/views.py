
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from django.http import HttpResponse

from lims.models import Task, Workflow
from rest_framework import viewsets
from lims.serializers import UserSerializer, GroupSerializer, TaskSerializer, WorkflowSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def register(request):
    """
    API endpoint that allows new user registration.
    """


def login(request):
    """
    API endpoint that allows login.
    """


def logout(request):
    """
    API endpoint that allows logout.
    """


def users(request):
    """
    API endpoint that returns all tasks.
    """
    return HttpResponse(User.objects.all())


def tasks(request):
    print('inside the tasks handler!')
    """
    API endpoint that returns all tasks.
    """
    return HttpResponse(Task.objects.all())


def workflows(request):
    """
    API endpoint that returns all workflows
    """
    return HttpResponse(Workflow.objects.all())
