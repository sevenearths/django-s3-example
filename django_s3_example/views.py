from django.http import HttpResponse, JsonResponse

from minio import Minio
from minio.error import BucketAlreadyExists, ResponseError, \
                        InvalidEndpointError, NoSuchKey

from .settings import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, \
                      MINIO_BUCKET, TEST_FILE, AWS_URL, AWS_ACCESS_KEY, \
                      AWS_SECRET_KEY, AWS_BUCKET, TEST_FILE


def minio_file_save_view(request):
    try:
        minio_client = Minio(
            MINIO_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
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
    file_url = minio_client.presigned_get_object(MINIO_BUCKET, TEST_FILE)
    return JsonResponse({'url': file_url})


def minio_file_load_view(request):
    try:
        minio_client = Minio(
            MINIO_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        message = {'message': 'incorrect minio url'}
        return JsonResponse(message, status=500)
    if not minio_client.bucket_exists(MINIO_BUCKET):
        message = {'message': 'bucket ('+MINIO_BUCKET+') does not exist'}
        return JsonResponse(message, status=500)
    try:
        minio_client.stat_object(MINIO_BUCKET, TEST_FILE)
    except NoSuchKey:
        message = {'message': 'file ('+TEST_FILE+') does not exist'}
        return JsonResponse(message, status=500)
    file_url = minio_client.presigned_get_object(MINIO_BUCKET, TEST_FILE)
    return JsonResponse({'url': file_url})

def s3_file_save_view(request):
    try:
        aws_client = Minio(
            AWS_URL,
            access_key=AWS_ACCESS_KEY,
            secret_key=AWS_SECRET_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        message = {'message': 'incorrect minio url'}
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
    file_url = aws_client.presigned_get_object(AWS_BUCKET, TEST_FILE)
    return JsonResponse({'url': file_url})

def s3_file_load_view(request):
    try:
        aws_client = Minio(
            AWS_URL,
            access_key=AWS_ACCESS_KEY,
            secret_key=AWS_SECRET_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        message = {'message': 'incorrect s3 url'}
        return JsonResponse(message, status=500)
    if not aws_client.bucket_exists(AWS_BUCKET):
        message = {'message': 'bucket ('+AWS_BUCKET+') does not exist'}
        return JsonResponse(message, status=500)
    try:
        aws_client.stat_object(AWS_BUCKET, TEST_FILE)
    except NoSuchKey:
        message = {'message': 'file ('+TEST_FILE+') does not exist'}
        return JsonResponse(message, status=500)
    file_url = aws_client.presigned_get_object(AWS_BUCKET, TEST_FILE)
    return JsonResponse({'url': file_url})
