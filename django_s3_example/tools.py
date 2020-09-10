from minio import Minio
from minio.error import InvalidEndpointError

from django_s3_example.settings import AWS_S3_ENDPOINT_URL, \
                                       AWS_STORAGE_BUCKET_NAME



def get_s3_public_url():
    if 'minio:9000' in AWS_S3_ENDPOINT_URL:
        return AWS_S3_ENDPOINT_URL.replace('minio', 'localhost') + '/' + AWS_STORAGE_BUCKET_NAME
    return AWS_S3_ENDPOINT_URL

def bucket_public_policy(bucket_name=AWS_STORAGE_BUCKET_NAME):
    return '''{
      "Version":"2012-10-17",
      "Statement":[
        {
          "Sid":"PublicRead",
          "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject","s3:GetObjectVersion"],
          "Resource":["arn:aws:s3:::{bucket}/*"]
        }
      ]
    }'''.replace('{bucket}', bucket_name)
