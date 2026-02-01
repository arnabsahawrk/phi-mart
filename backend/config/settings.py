from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-=s8^0+qo5c2mc$gf@du=i6*sbp3y=2&yh+3!e(gt-*-k#c$12o"

DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = "users.User"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "django_filters",
    "rest_framework",
    "djoser",
    "api",
    "product",
    "users",
    "order",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE


INTERNAL_IPS = ["127.0.0.1"]

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    # "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.IsAuthenticated",
    # ],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=25),
}

DJOSER = {
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "current_user": "users.serializers.UserSerializer",
    }
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token in this format: `JWT <your_token>`",
        },
    },
    "DOC_EXPANSION": "none",
    "DEFAULT_MODEL_RENDERING": "model",
    "SHOW_REQUEST_HEADERS": True,
}
