import json
import requests

from django.urls import reverse
from django.test import TestCase
from django.core.files.storage import default_storage

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError, InvalidEndpointError

from .settings import AWS_URL, AWS_ACCESS_KEY_ID, AWS_S3_ENDPOINT_URL, \
                      AWS_SECRET_ACCESS_KEY, TEST_FILE
from .tools import get_s3_public_url, bucket_public_policy
from .views import boto3_file_save_view


class Boto3FileSaveTest(TestCase):

    url          = None
    minio_client = None
    file_url     = None

    def setUp(self):
        self.url = reverse(boto3_file_save_view)
        self.file_url = get_s3_public_url() + '/' + TEST_FILE
        if default_storage.exists(TEST_FILE):
            default_storage.delete(TEST_FILE)

    def test_get_save_file_using_default_storage(self):
        response = requests.get(self.file_url.replace('localhost', 'minio'))
        # 404 = Minio, 403 = AWS S3
        self.assertRegex(str(response.status_code), '[404,403]')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertIn('url', json_response)

        self.assertEqual(self.file_url, json_response['url'])

        response = requests.get(self.file_url.replace('localhost', 'minio'))
        self.assertEqual(200, response.status_code)

        default_storage.delete(TEST_FILE)

        response = requests.get(self.file_url.replace('localhost', 'minio'))
        self.assertRegex(str(response.status_code), '[404,403]')
