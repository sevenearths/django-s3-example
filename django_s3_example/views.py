import logging

from django.http import HttpResponse, JsonResponse

from minio import Minio
from minio.error import BucketAlreadyExists, ResponseError, \
                        InvalidEndpointError, NoSuchKey

from .settings import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, \
                      MINIO_BUCKET, TEST_FILE

logger = logging.getLogger(__name__)


def file_save_view(request):
    return JsonResponse({'message': 'file saved'})

def file_load_view(request):
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
