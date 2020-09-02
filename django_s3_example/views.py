from django.http import HttpResponse, JsonResponse

from minio import Minio
from minio.error import BucketAlreadyExists, ResponseError, \
                        InvalidEndpointError, NoSuchKey

from .settings import MINIO_BUCKET, AWS_BUCKET, MINIO_URL_FILE, \
                      AWS_URL_FILE, TEST_FILE

from django_s3_example.tools import get_minio_client, get_aws_client


def minio_file_save_view(request):
    try:
        minio_client = get_minio_client()
    except InvalidEndpointError:
        message = {'message': 'incorrect minio url'}
        return JsonResponse(message, status=500)
    if not minio_client.bucket_exists(MINIO_BUCKET):
        message = {'message': 'bucket ('+MINIO_BUCKET+') does not exist'}
        return JsonResponse(message, status=500)
    try:
        minio_client.stat_object(MINIO_BUCKET, TEST_FILE)
    except NoSuchKey:
        minio_client.fput_object(
            MINIO_BUCKET, TEST_FILE,
            '/code/' + TEST_FILE
        )
    file_url = MINIO_URL_FILE + '/' + TEST_FILE
    return JsonResponse({'url': file_url})


def s3_file_save_view(request):
    try:
        aws_client = get_aws_client()
    except InvalidEndpointError:
        message = {'message': 'incorrect aws s3 url'}
        return JsonResponse(message, status=500)
    if not aws_client.bucket_exists(AWS_BUCKET):
        message = {'message': 'bucket ('+AWS_BUCKET+') does not exist'}
        return JsonResponse(message, status=500)
    try:
        aws_client.stat_object(AWS_BUCKET, TEST_FILE)
    except NoSuchKey:
        aws_client.fput_object(
            AWS_BUCKET, TEST_FILE,
            '/code/' + TEST_FILE
        )
    file_url = AWS_URL_FILE + '/' + TEST_FILE
    return JsonResponse({'url': file_url})
