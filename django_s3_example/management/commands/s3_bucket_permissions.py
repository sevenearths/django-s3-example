from django.core.management.base import BaseCommand, CommandError

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, \
                        InvalidEndpointError

from django_s3_example.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
                                       AWS_STORAGE_BUCKET_NAME

from django_s3_example.tools import bucket_public_policy


class Command(BaseCommand):
    help    = 'Creates a bucket and gives it public permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--aws',
            action='store_true',
            help='Use AWS S3',
        )

    def handle(self, *args, **options):
        url = 'minio:9000'
        if options['aws']:
            url = 's3.amazonaws.com'
        try:
            s3_client = Minio(
                url,
                access_key=AWS_ACCESS_KEY_ID,
                secret_key=AWS_SECRET_ACCESS_KEY,
                secure=False,
            )
        except InvalidEndpointError:
            raise CommandError('ERROR: Could not connect to Minio/S3 bucket server')
        try:
               s3_client.make_bucket(AWS_STORAGE_BUCKET_NAME)
        except BucketAlreadyOwnedByYou:
               print('INFO: Bucket already exists and is owned by you')
        except BucketAlreadyExists:
               print('INFO: Bucket already exists but my NOT be owned by you')

        try:
            s3_client.set_bucket_policy(
                AWS_STORAGE_BUCKET_NAME,
                bucket_public_policy(AWS_STORAGE_BUCKET_NAME)
            )
        except Exception:
            raise CommandError(
                'ERROR: Could not create policy on '+AWS_STORAGE_BUCKET_NAME+' bucket'
            )

        print('SUCCESS: Created bucket ' + AWS_STORAGE_BUCKET_NAME +
            ' and added public policy')
