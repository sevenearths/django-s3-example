import json
import requests

from django.urls import reverse
from django.test import TestCase

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError, InvalidEndpointError

from .settings import AWS_URL, AWS_ACCESS_KEY_ID, AWS_S3_ENDPOINT_URL, \
                      AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, TEST_FILE
from .tools import get_s3_public_url, bucket_public_policy
from .views import minio_file_save_view


class MinioFileSaveTest(TestCase):

    url          = None
    minio_client = None
    file_url     = None

    def setUp(self):
        self.url = reverse(minio_file_save_view)
        self.file_url = get_s3_public_url() + '/' + TEST_FILE
        # because we are getting it over the docker network
        try:
            self.minio_client = Minio(
                AWS_URL,
                access_key=AWS_ACCESS_KEY_ID,
                secret_key=AWS_SECRET_ACCESS_KEY,
                secure=False,
            )
        except InvalidEndpointError:
            raise CommandError('Could not connect to Minio')
        try:
            self.minio_client.make_bucket(AWS_STORAGE_BUCKET_NAME)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass
        try:
            self.minio_client.set_bucket_policy(
                AWS_STORAGE_BUCKET_NAME,
                bucket_public_policy()
            )
        except Exception:
            raise Exception('Unable to set public policy on bucket')
        self.minio_client.remove_object(AWS_STORAGE_BUCKET_NAME, TEST_FILE)

    def test_get_save_file_in_minio(self):
        docker_file_url = self.file_url.replace('localhost', 'minio')
        response = requests.get(docker_file_url)
        # 404 = Minio, 403 = AWS S3
        self.assertRegex(str(response.status_code), '[404,403]')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertIn('url', json_response)

        self.assertEqual(self.file_url, json_response['url'])

        response = requests.get(docker_file_url)
        self.assertEqual(200, response.status_code)

        self.minio_client.remove_object(AWS_STORAGE_BUCKET_NAME, TEST_FILE)

        response = requests.get(docker_file_url)
        self.assertRegex(str(response.status_code), '[404,403]')
