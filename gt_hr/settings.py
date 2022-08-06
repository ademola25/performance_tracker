import os
from django.contrib.messages import constants as messages
from celery.schedules import crontab
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv(
# 'SECRET_KEY', 'django-insecure-3@%3aunnd39_v0my7-luq93m*hx04s82og&umw-4sio&=cdrdf')
SECRET_KEY = 'django-insecure-3@%3aunnd39_v0my7-luq93m*hx04s82og&umw-4sio&=cdrdf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '172.18.1.107']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'celery',
    'django_celery_beat',
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_hotp',
    # 'django_otp.plugins.otp_static',



    # custom apps
    'accounts',
    "common",
    'manager',
    'hod',
    "hr_personnel",
    'department',
    'numbers_of_days',
    'trainee',
    'gt_logs',
    'comments',
    'axes',
]


CRISPY_TEMPLATE_PACK = 'uni_form'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utility.middleware.security.UserRestrictMiddleware',
    'utility.middleware.security.DisableClientSideCachingMiddleware',
    'ratelimit.middleware.RatelimitMiddleware',
    'axes.middleware.AxesMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'gt_hr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'gt_hr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.getenv('DB_NAME'),
        # 'USER': os.getenv('DB_USER'),
        # 'PASSWORD': os.getenv('DB_PASSWORD'),
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT', '5432'),
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
#TIME_ZONE = 'Africa/Lagos'



USE_I18N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'gt_hr/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')


BASE_URL = os.getenv('BASE_URL')

APP_WEBSITE = os.getenv('APP_WEBSITE')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
if DEBUG:
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_SSL = False


#from tut
# Redis and Celery Conf
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


CELERY_BEAT_SCHEDULE = {

    'yesterday_log_task': {
        'task': 'save_log_for_yesterday_and_check_approval_status',
        # 'schedule': crontab(minute=0, hour=0),
        # 'schedule': crontab(minute="*/1")
        # 'schedule': 30.0
        'schedule': crontab(minute=0, hour=0)

    },
    'eod_reminder_task': {
        'task': 'end_of_day_email_to_unlogged_trainee',
        # 'schedule': crontab(minute="*/1")
        'schedule': crontab(minute=0, hour=17, day_of_week="mon-fri")

    },
    'eoweek_reminder_task': {
        'task': 'friday_email_notification',
        # 'schedule': crontab(minute="*/1")
        'schedule': crontab(minute=0, hour=18, day_of_week="friday")
    }
}


FILE_UPLOAD_TYPE = '.csv'
MAX_UPLOAD_SIZE = 5242880
ENABLE_AD = False
AD_URL = ""

# RateLimit
RATELIMIT_ENABLE = True
RATELIMIT = '100/h'
LOGIN_RATELIMIT = '5/m'
RATELIMIT_VIEW = 'common.views.handler429'
# Axes Configuration
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_FAILURE_LIMIT = 5
AXES_RESET_ON_SUCCESS = True
AXES_VERBOSE = False
AXES_ENABLED = True
AXES_META_PRECEDENCE_ORDER = (
    'HTTP_X_REAL_IP',
    'REMOTE_ADDR',
)
AXES_ONLY_USER_FAILURES = True
AXES_COOLOFF_TIME = 24

# Session Timeout
SESSION_COOKIE_AGE = 72000
# X-Frame
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Cache
CONFIG_CACHE_TIMEOUT = 259200
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }

LOGIN_REDIRECT_URL = '/'

#session timeout
SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/'



# 2FA
OTP_TOTP_ISSUER = "UBAHCM"
ENABLE_2FA = False
