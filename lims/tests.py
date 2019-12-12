from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import DBProcessor
from .serializers import SongsSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_processor(name="", description="", file_type=""):
        if name != "" and file_type != "":
            DBProcessor.objects.create(name=name, file_type=file_type)

    def setUp(self):
        # add test data
        self.create_processor("proc1", ".txt")
        self.create_processor("proc2", ".csv")
        self.create_processor("proc3", ".xlsx")
        self.create_processor("proc4", ".csv")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_processors(self):
        """
        This test ensures that all processors added in the setUp method
        exist when we make a GET request to the processors/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = DBProcessor.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Create your tests here.
