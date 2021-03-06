
from pathlib import Path
from .my_settings import EMAIL, S3
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '*$32aaojr$%15egbonqy@aoo(ket!zt7j2z_zqgby1yqk$wid&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'x.x.x.x']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'feed_api.apps.FeedApiConfig',
    'notice_api.apps.NoticeApiConfig',
    'user_api.apps.UserApiConfig',
    'group_api.apps.GroupApiConfig',
    'notification_api.apps.NotificationApiConfig',
    'reports_api.apps.ReportsApiConfig',
    
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',

    'storages'
]

REST_FRAMEWORK = {

    # Web Test 때문에 꺼놈
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],


    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]

}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'main',
        # 'NAME': 'for_profile',
        'USER': 'dual_life',
        'PASSWORD': 'dual_life',
        'HOST': 'dual-life-instance.cezrhtu6o4hr.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',

    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# EMAIL SET
SITE_ID = 1

EMAIL_BACKEND = EMAIL['EMAIL_BACKEND']
EMAIL_PORT = EMAIL['EMAIL_PORT']
EMAIL_HOST = EMAIL['EMAIL_HOST']
EMAIL_HOST_USER = EMAIL['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = EMAIL['EMAIL_USE_TLS']


# AWS s3설정

AWS_ACCESS_KEY_ID = S3['access_key']
AWS_SECRET_ACCESS_KEY = S3['secret_key']
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'loopus'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024000000  # value in bytes 1GB here
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024000000

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AUTH_USER_MODEL = 'user_api.UserCustom'
