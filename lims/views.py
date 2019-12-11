import logging
from django.shortcuts import render
from django.contrib.auth.models import User, Group

from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from lims.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Hello world")
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
