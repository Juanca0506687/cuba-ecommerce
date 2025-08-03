#!/usr/bin/env python
"""
Script para generar una clave secreta segura para Django
"""
import secrets
import string

def generate_secret_key(length=50):
    """Genera una clave secreta segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("🔐 Clave secreta generada para producción:")
    print(f"SECRET_KEY = '{secret_key}'")
    print("\n📋 Copia esta clave y úsala en tu configuración de producción.")
    print("⚠️  IMPORTANTE: Nunca compartas esta clave públicamente.") 