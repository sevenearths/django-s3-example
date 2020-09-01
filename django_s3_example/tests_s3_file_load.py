import json
import requests

from django.urls import reverse
from django.test import TestCase

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError, NoSuchKey

from .settings import AWS_URL, AWS_ACCESS_KEY, AWS_SECRET_KEY, \
                      AWS_BUCKET, TEST_FILE

from django_s3_example.views import s3_file_load_view


class S3FileLoadTest(TestCase):

    url          = None
    aws_client = None

    def setUp(self):
        self.url = reverse(s3_file_load_view)
        self.aws_client = Minio(
            AWS_URL,
            access_key=AWS_ACCESS_KEY,
            secret_key=AWS_SECRET_KEY,
            secure=False,
        )
        try:
            self.aws_client.make_bucket(AWS_BUCKET)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass

        try:
            self.aws_client.fget_object(AWS_BUCKET, TEST_FILE, '/code/' + TEST_FILE)
        except NoSuchKey:
            self.aws_client.fput_object(AWS_BUCKET, TEST_FILE, '/code/' + TEST_FILE)

    def test_get_load_file_in_s3(self):
        self.assertTrue(True)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        file_url = json_response['url']

        response = requests.get(file_url)
        self.assertEqual(200, response.status_code)

        self.aws_client.remove_object(AWS_BUCKET, TEST_FILE)

        response = requests.get(file_url)
        self.assertEqual(404, response.status_code)
