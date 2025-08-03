"""
Configuración de producción para el e-commerce cubano
"""
import os
from pathlib import Path
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-production-key-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Configuración de hosts permitidos para producción
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',  # Cambiar por tu dominio
    'localhost',
    '127.0.0.1',
]

# Configuración de seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de archivos estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Configuración de archivos de media
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Configuración de base de datos para producción (SQLite por ahora)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de logging para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Configuración de caché (opcional para mejorar rendimiento)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Configuración de sesiones
SESSION_COOKIE_SECURE = False  # Cambiar a True si usas HTTPS
CSRF_COOKIE_SECURE = False     # Cambiar a True si usas HTTPS

# Configuración de archivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuración de WhatsApp (mantener la misma)
WHATSAPP_NUMBER = "5359705886"
WHATSAPP_MESSAGE_TEMPLATE = """
🛒 *NUEVA ORDEN - {order_number}*

👤 *CLIENTE:*
{user_name}
📞 {phone}

📦 *PRODUCTOS:*
{products}

💰 *TOTAL: {total}*

{delivery_info}

📝 *NOTAS:*
{notes}

⏰ *FECHA:* {date}
""" 