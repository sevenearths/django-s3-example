from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage

from minio import Minio
from minio.error import BucketAlreadyExists, ResponseError, \
                        InvalidEndpointError, NoSuchKey

from botocore.exceptions import EndpointConnectionError, ClientError

from .settings import AWS_URL, AWS_ACCESS_KEY_ID, AWS_S3_ENDPOINT_URL, \
                      AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, TEST_FILE

from .tools import get_s3_public_url


def minio_file_save_view(request):
    try:
        minio_client = Minio(
            AWS_URL,
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=AWS_SECRET_ACCESS_KEY,
            secure=False,
        )
    except InvalidEndpointError:
        message = {'message': 'incorrect minio url'}
        return JsonResponse(message, status=500)
    if not minio_client.bucket_exists(AWS_STORAGE_BUCKET_NAME):
        message = {'message': 'bucket ('+AWS_STORAGE_BUCKET_NAME+') does not exist'}
        return JsonResponse(message, status=500)
    try:
        minio_client.stat_object(AWS_STORAGE_BUCKET_NAME, TEST_FILE)
    except NoSuchKey:
        minio_client.fput_object(
            AWS_STORAGE_BUCKET_NAME, TEST_FILE,
            '/code/' + TEST_FILE
        )
    file_url = get_s3_public_url() + '/' + TEST_FILE
    return JsonResponse({'url': file_url})


def boto3_file_save_view(request):
    try:
        file = File(open(TEST_FILE, 'rb'))
        default_storage.save(TEST_FILE, file)
    except EndpointConnectionError:
        message = {'message':'Could not connect to s3 storage'}
        return JsonResponse(message, status=400)
    except ClientError as e:
        message = {'message':'Incorrect access key or access key secret'}
        if 'NoSuchBucket' in str(type(e)):
            message = {'message':'bucket does not exist'}
        return JsonResponse(message, status=400)
    file_url = get_s3_public_url() + '/' + TEST_FILE
    return JsonResponse({'url': file_url})
