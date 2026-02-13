"""
Django settings for config project.
Django 5.2.x
Production-ready configuration (Render / DigitalOcean friendly)
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------
ENV = os.getenv("DJANGO_ENV", "dev")  # dev / prod
DEBUG = ENV != "prod"

# Prod'da SECRET_KEY env'den gelsin (yoksa crash etsin)
if DEBUG:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "django-insecure-rr^wgz70%pjwr&xr1uk4vnr@ook^@3m!(a5nyue&=@f3qp^&o!"
    )
else:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is required in production (set env SECRET_KEY).")

# Site URL (WhatsApp / ürün linkleri vs.)
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000" if DEBUG else "https://otoparca-2.onrender.com")

# ---------------------------------------------------
# HOSTS / CSRF
# ---------------------------------------------------
# Örn env:
# ALLOWED_HOSTS=otoparca-2.onrender.com,umayotoyedekparca.com,www.umayotoyedekparca.com
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Örn env:
# CSRF_TRUSTED_ORIGINS=https://otoparca-2.onrender.com,https://umayotoyedekparca.com,https://www.umayotoyedekparca.com
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

    # ✅ Static dosyaları prod’da sorunsuz servis etmek için
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
# Başlangıç için SQLite (Render'da deploy sonrası dosya kalıcılığı sınırlı olabilir)
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
# STATIC / MEDIA
# ---------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Dev’de local static klasörün
STATICFILES_DIRS = [BASE_DIR / "static"]

# Prod’da collectstatic buraya toplar
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise cache'li static (opsiyonel ama iyi)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------
# SECURITY (Prod)
# ---------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ---------------------------------------------------
# BUSINESS INFO (contact strip)
# ---------------------------------------------------
BUSINESS_NAME = "OtoParça"
BUSINESS_ADDRESS = "Ataşehir, İstanbul"
BUSINESS_PHONE = "+90 532 000 00 00"
BUSINESS_EMAIL = "iletisim@otoparca.com"

MAP_EMBED_SRC = os.getenv("MAP_EMBED_SRC", "https://www.google.com/maps/embed?pb=YOUR_EMBED_CODE")
