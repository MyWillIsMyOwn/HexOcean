import os
from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status

from .models import Image, User
from .serializers import ImageSerializer
import requests

from unittest.mock import MagicMock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class ImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("main.views.post")
    def test_upload_jpg_file(self, mock_handle_uploaded_file):
        mock_handle_uploaded_file.return_value = "test.jpg"
        with open("main/images_for_testing/test.jpg", "rb") as file:
            response = self.client.post("/upload/", {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)

    # def test_upload_png_file(self):
    #     file_path = os.path.join(
    #         os.path.dirname(os.path.abspath(__file__)), "test_files", "test.png"
    #     )
    #     with open(file_path, "rb") as f:
    #         data = {
    #             "file": SimpleUploadedFile(f.name, f.read(), content_type="image/png")
    #         }
    #         response = self.client.post("/upload/", data=data, format="multipart")
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertTrue(Image.objects.filter(name=f.name).exists())

    # def test_upload_non_image_file(self):
    #     file_path = os.path.join(
    #         os.path.dirname(os.path.abspath(__file__)), "test_files", "test.txt"
    #     )
    #     with open(file_path, "rb") as f:
    #         data = {
    #             "file": SimpleUploadedFile(f.name, f.read(), content_type="text/plain")
    #         }
    #         response = self.client.post("/upload/", data=data, format="multipart")
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_upload_corrupted_image_file(self):
    #     data = BytesIO()
    #     Image.new("RGB", (100, 100)).save(data, format="JPEG")
    #     # simulate a corrupted file by changing the last byte
    #     file_data = data.getvalue()[:-1] + b"0"
    #     data = {
    #         "file": SimpleUploadedFile("test.jpg", file_data, content_type="image/jpeg")
    #     }
    #     response = self.client.post("/upload/", data=data, format="multipart")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
