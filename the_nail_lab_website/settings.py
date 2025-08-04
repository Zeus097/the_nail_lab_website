from decouple import config, Csv
from dotenv import load_dotenv
import os
from pathlib import Path
import sys
import dj_database_url
from django.conf.urls import static
from django.urls import reverse_lazy



#  ENVIRONMENT SETUP
# ===============================
ENVIRONMENT = os.environ.get("DJANGO_ENV", "development").lower()
if ENVIRONMENT == "development":
    load_dotenv()


#  BASE PATHS
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent



#  SECURITY
# ===============================
SECRET_KEY = config('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")

DEBUG = config('DEBUG', default='False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())



#  APPLICATIONS
# ===============================
GOOGLE_AUTHENTICATION = [
    'social_django',
]

PROJECT_APPS = [
    'studio',
    'accounts.apps.AccountsConfig',  # BECAUSE OF THE SIGNAL, TO PREVENT ERROR DUPLICATION WHEN MIGRATING
    'services',
    'photos',
    'appointments',
    'storages',  # Required for django-storages
    'cloudinary',
    'cloudinary_storage',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + PROJECT_APPS + GOOGLE_AUTHENTICATION



# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # GOOGLE
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'the_nail_lab_website.urls'



#  TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'studio.context_processors.user_role_context',
                # To show in nav bar rest day for employee on every page.
                # Without this setting, it shows rest day only on homepage!

                # GOOGLE
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'the_nail_lab_website.wsgi.application'



#  AUTHENTICATION
# ===============================
AUTHENTICATION_BACKENDS = [
    'accounts.authentication.LogInWithEmail',
    'django.contrib.auth.backends.ModelBackend',

    # GOOGLE BACKENDS
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]



#  DATABASE CONFIG
# ===============================
if ENVIRONMENT == "production":
    DATABASES = {
        'default': dj_database_url.config(
            default=f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}",
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }



#  PASSWORD VALIDATORS
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]



#  LOCALIZATION
# ===============================
LANGUAGE_CODE = 'bg'
TIME_ZONE = 'Europe/Sofia'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('bg', 'Български'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'accounts' / 'locale',
]



#  SECURITY COOKIES
# ===============================
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default='False').lower() in ('true', '1', 'yes')
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default='False').lower() in ('true', '1', 'yes')
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default='False').lower() in ('true', '1', 'yes')


#  STATIC / MEDIA FILES
# ===============================
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / 'static']


# MEDIA_URL = '/media/'  #  --> Empty for Cloudinary in Production
MEDIA_ROOT = BASE_DIR / 'media'



#  PRIMARY KEY TYPE
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#  CUSTOM USER MODEL
# ===============================
AUTH_USER_MODEL = 'accounts.BaseUser'
LOGIN_REDIRECT_URL = reverse_lazy('homepage')
LOGOUT_REDIRECT_URL = reverse_lazy('login')



#  GOOGLE OAUTH2 SETTINGS
# ===============================
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('homepage')
SOCIAL_AUTH_REDIRECT_IS_HTTPS = ENVIRONMENT == "production"


if ENVIRONMENT == "production":
    SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'https://the-nail-lab.onrender.com/complete/google-oauth2/'
else:
    SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/auth/complete/google-oauth2/'



SOCIAL_AUTH_PIPELINE = [

    # 1. Get info from Google
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',

    # 2. IF there is a user with this email → CONNECT
    'social_core.pipeline.social_auth.associate_by_email',  # FIX: if email already exists

    # 3. Preparing the user
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',

    # 4. Connecting social account with the user
    'social_core.pipeline.social_auth.associate_user',

    # 5. CUSTOM LOGIC (safe, already has `user`)
    'accounts.pipeline.create_client_profile',  # Creating client
    'accounts.pipeline.check_profile_data',     # Redirecting if no password/ph. number

    # 6. Loading additional data
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

# CLOUDINARY FOR media storage
# =================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'





# Helps social_django generate absolute URLs correctly
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'




MAILJET_API_KEY = config('MAILJET_API_KEY')
MAILJET_API_SECRET = config('MAILJET_API_SECRET')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')









