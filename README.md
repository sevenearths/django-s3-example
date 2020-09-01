## Installing

### Docker

Docker

https://docs.docker.com/install/linux/docker-ce/ubuntu/

Docker-compose

https://docs.docker.com/compose/install/

## Setting up

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
AWS_URL          = 's3.amazonaws.com'
AWS_ACCESS_KEY   = '...'
AWS_SECRET_KEY   = '...'
AWS_BUCKET       = '...'
...
# docker-compose up
```

## Starting up

```
# docker-compose up
...
```

## Tests

Then in a seperate window run

```
# docker-compose exec app python manage.py test
```
