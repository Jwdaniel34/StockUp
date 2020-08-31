import os

ALLOWED_HOSTS_ENV = os.environ.get('DJANGO_ALLOWED_HOSTS').split(" ")

print(ALLOWED_HOSTS_ENV)