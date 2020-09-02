from minio import Minio
from minio.error import InvalidEndpointError

from django_s3_example.settings import MINIO_URL,MINIO_ACCESS_KEY, \
                                       MINIO_SECRET_KEY, MINIO_BUCKET, \
                                       MINIO_URL_FILE, AWS_URL, \
                                       AWS_ACCESS_KEY, AWS_SECRET_KEY, \
                                       AWS_BUCKET, AWS_REGION, AWS_URL_FILE

def get_minio_client():
    try:
        return Minio(
            MINIO_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        raise CommandError('Could not connect to Minio')

def get_aws_client():
    try:
        return Minio(
            AWS_URL,
            access_key=AWS_ACCESS_KEY,
            secret_key=AWS_SECRET_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        raise CommandError('Could not connect to AWS S3')

def bucket_public_policy(bucket_name):
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
