#!/usr/bin/env python
"""
Script para preparar el proyecto Django para producción
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Error: {e.stderr}")
        return False

def create_directories():
    """Crea directorios necesarios para producción"""
    directories = ['logs', 'staticfiles', 'media']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Directorio '{directory}' creado/verificado")

def main():
    """Función principal"""
    print("🚀 Preparando proyecto Django para producción...")
    
    # Crear directorios necesarios
    create_directories()
    
    # Comandos para preparar producción
    commands = [
        ("python manage.py collectstatic --noinput", "Recolectando archivos estáticos"),
        ("python manage.py check --deploy", "Verificando configuración de producción"),
        ("python manage.py makemigrations", "Creando migraciones"),
        ("python manage.py migrate", "Aplicando migraciones"),
    ]
    
    # Ejecutar comandos
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Error durante la preparación. Revisa los errores arriba.")
            sys.exit(1)
    
    print("\n🎉 ¡Proyecto preparado para producción!")
    print("\n📋 Próximos pasos:")
    print("1. Crear cuenta en PythonAnywhere.com")
    print("2. Subir archivos al servidor")
    print("3. Configurar variables de entorno")
    print("4. Configurar dominio")

if __name__ == "__main__":
    main() 