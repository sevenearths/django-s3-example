import json
import requests

from django.urls import reverse
from django.test import TestCase

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError

from .settings import MINIO_BUCKET, MINIO_URL_FILE, TEST_FILE
from .tools import bucket_public_policy, get_minio_client
from .views import minio_file_save_view


class MinioFileSaveTest(TestCase):

    url          = None
    minio_client = None
    file_url     = None

    def setUp(self):
        self.url = reverse(minio_file_save_view)
        self.file_url = MINIO_URL_FILE + '/' + TEST_FILE
        # because we are getting it over the docker network
        self.minio_client = get_minio_client()
        try:
            self.minio_client.make_bucket(MINIO_BUCKET)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass
        try:
            self.minio_client.set_bucket_policy(
                MINIO_BUCKET,
                bucket_public_policy(MINIO_BUCKET)
            )
        except Exception:
            raise Exception('Unable to set public policy on bucket')
        self.minio_client.remove_object(MINIO_BUCKET, TEST_FILE)

    def test_get_save_file_in_minio(self):
        docker_file_url = self.file_url.replace('localhost', 'minio')
        response = requests.get(docker_file_url)
        self.assertEqual(404, response.status_code)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertIn('url', json_response)

        self.assertEqual(self.file_url, json_response['url'])

        response = requests.get(docker_file_url)
        self.assertEqual(200, response.status_code)

        self.minio_client.remove_object(MINIO_BUCKET, TEST_FILE)

        response = requests.get(docker_file_url)
        self.assertEqual(404, response.status_code)
