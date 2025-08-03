# 🚀 Guía de Despliegue en Producción - E-commerce Cubano

## 📋 Requisitos Previos

- ✅ Proyecto Django funcionando localmente
- ✅ Cuenta en PythonAnywhere.com (gratuita)
- ✅ Git instalado (opcional pero recomendado)

## 🔧 Paso 1: Preparar el Proyecto Localmente

### 1.1 Ejecutar el script de preparación
```bash
python prepare_production.py
```

### 1.2 Verificar que todo funciona
```bash
python manage.py runserver
```

## 🌐 Paso 2: Crear Cuenta en PythonAnywhere

### 2.1 Ir a PythonAnywhere
- Visita: https://www.pythonanywhere.com
- Haz clic en "Create a Beginner account" (GRATIS)
- Completa el registro

### 2.2 Acceder a tu cuenta
- Inicia sesión en tu cuenta
- Ve al Dashboard

## 📤 Paso 3: Subir Archivos al Servidor

### 3.1 Usando Git (Recomendado)
```bash
# En tu computadora local
git init
git add .
git commit -m "Primera versión para producción"
git remote add origin https://github.com/tuusuario/cuba-ecommerce.git
git push -u origin main
```

### 3.2 En PythonAnywhere
1. Ve a la pestaña "Files"
2. Navega a `/home/tuusuario/`
3. Abre una consola Bash
4. Ejecuta:
```bash
git clone https://github.com/tuusuario/cuba-ecommerce.git
cd cuba-ecommerce
```

### 3.3 Usando Upload Manual
1. En PythonAnywhere, ve a "Files"
2. Navega a `/home/tuusuario/`
3. Crea una carpeta llamada `cuba-ecommerce`
4. Sube todos los archivos del proyecto

## ⚙️ Paso 4: Configurar el Entorno

### 4.1 Instalar dependencias
En la consola de PythonAnywhere:
```bash
cd cuba-ecommerce
pip install --user -r requirements.txt
```

### 4.2 Configurar variables de entorno
En la consola:
```bash
export SECRET_KEY="tu-clave-secreta-muy-segura"
export DJANGO_SETTINGS_MODULE="cuba_ecommerce.settings_production"
```

### 4.3 Aplicar migraciones
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🌍 Paso 5: Configurar la Aplicación Web

### 5.1 Crear aplicación web
1. Ve a la pestaña "Web"
2. Haz clic en "Add a new web app"
3. Selecciona "Manual configuration"
4. Selecciona Python 3.9 o superior

### 5.2 Configurar el código
En la sección "Code":
- **Source code**: `/home/tuusuario/cuba-ecommerce`
- **Working directory**: `/home/tuusuario/cuba-ecommerce`

### 5.3 Configurar WSGI
Haz clic en el archivo WSGI y reemplaza el contenido con:
```python
import os
import sys

# Agregar el path del proyecto
path = '/home/tuusuario/cuba-ecommerce'
if path not in sys.path:
    sys.path.append(path)

# Configurar variables de entorno
os.environ['SECRET_KEY'] = 'tu-clave-secreta-muy-segura'
os.environ['DJANGO_SETTINGS_MODULE'] = 'cuba_ecommerce.settings_production'

# Importar la aplicación Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5.4 Configurar archivos estáticos
En la sección "Static files":
- **URL**: `/static/`
- **Directory**: `/home/tuusuario/cuba-ecommerce/staticfiles`

## 🔐 Paso 6: Crear Superusuario

En la consola de PythonAnywhere:
```bash
cd cuba-ecommerce
python manage.py createsuperuser
```

## 🎯 Paso 7: Probar la Aplicación

### 7.1 Verificar que funciona
1. Ve a tu dominio: `https://tuusuario.pythonanywhere.com`
2. Verifica que la página principal carga
3. Prueba el registro de usuarios
4. Prueba el login del admin

### 7.2 Configurar dominio personalizado (Opcional)
1. Ve a la pestaña "Web"
2. En "Domains", agrega tu dominio personalizado
3. Configura los DNS de tu dominio

## 🔧 Configuración Adicional

### Base de Datos PostgreSQL (Opcional)
Para mejor rendimiento, puedes cambiar a PostgreSQL:
```bash
pip install psycopg2-binary
```

Y actualizar `settings_production.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configurar HTTPS
1. Ve a la pestaña "Web"
2. En "Security", habilita HTTPS
3. Actualiza `SESSION_COOKIE_SECURE = True` en settings

## 🚨 Solución de Problemas

### Error 500
1. Revisa los logs en la pestaña "Web"
2. Verifica que todas las dependencias están instaladas
3. Asegúrate de que DEBUG = False en producción

### Error de archivos estáticos
1. Ejecuta `python manage.py collectstatic`
2. Verifica la configuración de STATIC_ROOT
3. Revisa los permisos de archivos

### Error de base de datos
1. Verifica que las migraciones están aplicadas
2. Revisa la configuración de DATABASES
3. Asegúrate de que la base de datos existe

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en PythonAnywhere
2. Verifica la configuración paso a paso
3. Consulta la documentación de Django

## 🎉 ¡Listo!

Tu e-commerce cubano está ahora en línea y disponible para usuarios reales.

**URL de tu sitio**: `https://tuusuario.pythonanywhere.com`

**Panel de administración**: `https://tuusuario.pythonanywhere.com/admin` 