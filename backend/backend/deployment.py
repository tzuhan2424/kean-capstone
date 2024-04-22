import os 
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]

DEBUG = False
SECRET_KEY=os.environ['MY_SECRET_KEY']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# this should be frontend
CORS_ALLOWED_ORIGINS = [
    "https://gentle-tree-0c507cb0f.5.azurestaticapps.net"
]

CONNECTION = os.environ['AZURE_CONNECTIONSTRING']
CON_STR = {pair.split('=')[0]:pair.split('=')[1] for pair in CONNECTION.split(' ')}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CON_STR['DB_NAME'],  # Use your database name here
        'USER': CON_STR['DB_USER'],  # Your MySQL username
        'PASSWORD': CON_STR['DB_PASSWORD'],  # Your MySQL user password
        'HOST': CON_STR['HOST'],  # Your database host
        'PORT': '3306',  # Default MySQL port
    }
}

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')