import json
import requests
from django.test import TestCase

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError

from .settings import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, \
                      MINIO_BUCKET, TEST_FILE


class MinioFileLoadTest(TestCase):

    url          = '/file/load/'
    file_url     = None
    minio_client = None

    def setUp(self):
        self.minio_client = Minio(
            MINIO_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
        try:
            self.minio_client.make_bucket(MINIO_BUCKET)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass
        self.minio_client.fput_object(MINIO_BUCKET, TEST_FILE, '/code/' + TEST_FILE)

    def test_simple(self):
        response = self.client.get(self.file_url)
        self.assertEqual(404, response.status_code)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        file_url = json_response['url']

        response = requests.get(file_url)
        self.assertEqual(200, response.status_code)

        self.minio_client.remove_object(MINIO_BUCKET, TEST_FILE)

        response = requests.get(file_url)
        self.assertEqual(404, response.status_code)
