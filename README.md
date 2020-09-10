## Idea

![Alt text](/save_store_retrieve.png?raw=true "Preview")

Best have the files served up by S3. This will free up your app to work on business logic and other things.

## Installing

### Docker

Docker

https://docs.docker.com/install/linux/docker-ce/ubuntu/

Docker-compose

https://docs.docker.com/compose/install/

## Setting up

### Aws

[Instructions](amazon-s3-setup.html) on how to setup S3 and IAM for this project

> Following the above guide should give you a policy similar to [this](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#iam-policy "IAM policies on AWS")

### Local Development

```
# python
>>> import random, string
>>> ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)])
'<secret_key>'
>>> exit()
# cd django_s3_example
# cp settings.py.example settings.py
# vim settings.py
...
SECRET_KEY = '<secret_key>'
...
```

## Starting up

```
# docker-compose up
...
```

## Tests

Then in a separate window run

### Minio Library

```
# docker-compose exec app python manage.py test
```

### Boto3 Library *(django.core.files.storage.default_storage)*

```
# vim django_s3_example/settings.py
...
AWS_ACCESS_KEY_ID       = '...'
AWS_SECRET_ACCESS_KEY   = '...'
AWS_STORAGE_BUCKET_NAME = '...'
AWS_S3_REGION_NAME      = '...'
...
# docker-compose exec app python manage.py test
```
