"""
Django settings for config project.
Django 5.2.x
Production-ready configuration (Render / DigitalOcean friendly)
"""

from pathlib import Path
import os
import cloudinary


BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------
ENV = os.getenv("DJANGO_ENV", "dev")  # dev / prod
DEBUG = ENV != "prod"

# SECRET KEY
if DEBUG:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "django-insecure-rr^wgz70%pjwr&xr1uk4vnr@ook^@3m!(a5nyue&=@f3qp^&o!"
    )
else:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is required in production (set env SECRET_KEY).")

# SITE URL (WhatsApp / ürün linkleri vs.)
if DEBUG:
    SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
else:
    SITE_URL = os.getenv("SITE_URL")
    if not SITE_URL:
        raise RuntimeError("SITE_URL is required in production (set env SITE_URL).")

# ---------------------------------------------------
# HOSTS / CSRF
# ---------------------------------------------------
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(",") if x.strip()]

# Render / reverse proxy arkasında HTTPS doğru algılansın
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------
# APPS
# ---------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "products",
]

# ---------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------
# TEMPLATES
# ---------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.business_info",
            ],
        },
    },
]

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------
# AUTH PASSWORD VALIDATORS
# ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------
# I18N / TZ
# ---------------------------------------------------
LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------
# STATIC
# ---------------------------------------------------
STATIC_URL = "/static/"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]
else:
    STATICFILES_DIRS = []

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------
# MEDIA (✅ Cloudinary - ücretsiz çözüm)
# ---------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # local dev için (prod'da Cloudinary kullanacağız)

USE_CLOUDINARY = (not DEBUG) and bool(os.getenv("CLOUDINARY_CLOUD_NAME"))

if USE_CLOUDINARY:
    # Cloudinary storage kullan
    INSTALLED_APPS += [
        "cloudinary",
        "cloudinary_storage",
    ]

    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------
# SECURITY (Prod)
# ---------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

