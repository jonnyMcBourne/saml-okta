from pathlib import Path
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST,xmldsig
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# asi es como lo pone en la documentacion de saml
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#(f1mc&u3ayqv1sx4$%vo=n)f(le6+gt1tm5sf&57)(m$c=*n6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangosaml2",
    "user",
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

ROOT_URLCONF = "samltest.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "samltest.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


##SAMl CONFIGURATION
import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAML_CONFIG = {
    'xmlsec_binary': '/usr/local/bin/xmlsec1',  # Ajusta esta ruta si es necesario
    'entityid': 'http://127.0.0.1:8000/saml2/metadata/',
    'allow_unknown_attributes': True,
    'service': {    
        'sp': {
            'name': 'Django SP',
            'endpoints': {
                'assertion_consumer_service': [
                    ('http://127.0.0.1:8000/saml2/acs/',BINDING_HTTP_POST),
                ],
                'single_logout_service': [
                    ('http://127.0.0.1:8000/saml2/ls/', BINDING_HTTP_REDIRECT),
                ],
            },
            'allow_unsolicited': True,
            'authn_requests_signed': False,
            'logout_requests_signed': True,
            'want_assertions_signed': True,
            'want_response_signed': False,

            'signing_algorithm': xmldsig.SIG_RSA_SHA256,
            'digest_algorithm':  xmldsig.DIGEST_SHA256,
                 # Mandates that the identity provider MUST authenticate the
            # presenter directly rather than rely on a previous security context.
            'force_authn': False,

            # Enable AllowCreate in NameIDPolicy.
            'name_id_format_allow_create': False,

            # attributes that this project need to identify a user
            'required_attributes': ['email',],
            #'optional_attributes': ['eduPersonAffiliation'],
        },
    },
    'metadata': {
        'local': [join(BASE_DIR, 'metadata.xml')], # esto es cuando el metadata esta en el local 
        #'remote':[
        #    {
        #        "url":"https://dev-93915284.okta.com/app/exkhew6c38eQMnQ855d7/sso/saml/metadata",
        #        "certfile":os.path.join(BASE_DIR,'certs','okta.certs')
        #    }
        #]
    },
    'debug': True,
    'key_file': join(BASE_DIR, 'private_key.key'),  # Ajusta esta ruta si es necesario
    'cert_file': join(BASE_DIR, 'public_cert.cert'),  # Ajusta esta ruta si es necesario
    'encryption_keypairs': [{
        'key_file': join(BASE_DIR, 'private_key.key'),  # Ajusta esta ruta si es necesario
        'cert_file': join(BASE_DIR, 'public_cert.cert'),  # Ajusta esta ruta si es necesario
    }],
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)
SAML_ATTRIBUTE_MAPPING = {
    'email': ('email',),
}

SAML_CSP_HANDLER=""
SAML_SESSION_COOKIE_NAME = 'saml_session'
SAML_SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
LOGIN_REDIRECT_URL="/admin"

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'djangosaml2': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

#MODIFICACION PARA  USER APP
AUTH_USER_MODEL='user.User'
