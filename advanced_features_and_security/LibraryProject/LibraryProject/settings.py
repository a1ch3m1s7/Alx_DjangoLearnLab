"""
Security Configurations:
- DEBUG is False for production
- ALLOWED_HOSTS set to restrict domains
- Secure headers for XSS, CSRF, cookies, and clickjacking
- HSTS enabled to enforce HTTPS
- Content Security Policy (CSP) via django-csp
"""
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a0anyjf!k+h+&^5cpnwreok4+rn-w5&v436_o0%$0b7)o(=p0x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # set to False in production
ALLOWED_HOSTS = ["127.0.0.1"]  # add hosts you serve

# Keep SECRET_KEY secret; load from env in production
# SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# --- Secure cookies ---
SESSION_COOKIE_SECURE = True     # only send session cookie over HTTPS
CSRF_COOKIE_SECURE = True        # only send CSRF cookie over HTTPS
SESSION_COOKIE_HTTPONLY = True   # prevent JS access to session cookie
CSRF_COOKIE_HTTPONLY = False     # CSRF cookie must be readable by JavaScript for some APIs; usually False

# --- Clickjacking, XSS protections, Mime sniffing ---
X_FRAME_OPTIONS = "DENY"                    # prevents clickjacking
SECURE_BROWSER_XSS_FILTER = True            # sets X-XSS-Protection header (legacy but OK)
SECURE_CONTENT_TYPE_NOSNIFF = True          # sets X-Content-Type-Options: nosniff

# --- HSTS (only if serving HTTPS) ---
SECURE_HSTS_SECONDS = 31536000   # 1 year - enable only after HTTPS validated
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# redirect all HTTP -> HTTPS (enable with HTTPS)
SECURE_SSL_REDIRECT = True

# --- Misc ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # if behind proxy/load-balancer



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf'
    'csp',
]

AUTH_USER_MODEL = "bookshelf.CustomUser"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "list_book"
LOGOUT_REDIRECT_URL = "login"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "csp.middleware.CSPMiddleware",
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")
ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
