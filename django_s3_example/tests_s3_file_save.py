import json
import requests

from django.urls import reverse
from django.test import TestCase

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        ResponseError

from .settings import AWS_URL, AWS_ACCESS_KEY, AWS_SECRET_KEY, \
                      AWS_BUCKET, TEST_FILE

from .settings import AWS_BUCKET, AWS_URL_FILE, TEST_FILE
from .tools import bucket_public_policy, get_aws_client
from .views import s3_file_save_view


class S3FileSaveTest(TestCase):

    url        = None
    aws_client = None
    file_url   = None

    def setUp(self):
        self.url = reverse(s3_file_save_view)
        self.file_url = AWS_URL_FILE + '/' + TEST_FILE
        self.aws_client = get_aws_client()
        try:
            self.aws_client.make_bucket(AWS_BUCKET)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass
        try:
            self.aws_client.set_bucket_policy(
                AWS_BUCKET,
                bucket_public_policy(AWS_BUCKET)
            )
        except Exception:
            raise Exception('Unable to set public policy on bucket')
        self.aws_client.remove_object(AWS_BUCKET, TEST_FILE)

    def test_get_save_file_in_s3(self):
        response = requests.get(self.file_url)
        self.assertEqual(403, response.status_code)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertIn('url', json_response)

        self.assertEqual(self.file_url, json_response['url'])

        response = requests.get(self.file_url)
        self.assertEqual(200, response.status_code)

        self.aws_client.remove_object(AWS_BUCKET, TEST_FILE)

        response = requests.get(self.file_url)
        self.assertEqual(403, response.status_code)
