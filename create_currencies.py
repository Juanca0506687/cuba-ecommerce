#!/usr/bin/env python
"""
Script para crear las monedas iniciales del sistema
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuba_ecommerce.settings')
django.setup()

from store.models import Currency

def create_currencies():
    """Crea las monedas iniciales del sistema"""
    
    currencies_data = [
        {
            'code': 'CUP',
            'name': 'Peso Cubano',
            'symbol': '₱',
            'exchange_rate': 1.0000,
            'is_active': True,
            'is_default': True
        },
        {
            'code': 'USD',
            'name': 'Dólar Estadounidense',
            'symbol': '$',
            'exchange_rate': 0.0417,  # 1 USD = 24 CUP (aproximado)
            'is_active': True,
            'is_default': False
        },
        {
            'code': 'EUR',
            'name': 'Euro',
            'symbol': '€',
            'exchange_rate': 0.0385,  # 1 EUR = 26 CUP (aproximado)
            'is_active': True,
            'is_default': False
        },
        {
            'code': 'MXN',
            'name': 'Peso Mexicano',
            'symbol': '$',
            'exchange_rate': 0.7692,  # 1 MXN = 1.3 CUP (aproximado)
            'is_active': True,
            'is_default': False
        },
        {
            'code': 'CAD',
            'name': 'Dólar Canadiense',
            'symbol': 'C$',
            'exchange_rate': 0.0308,  # 1 CAD = 32.5 CUP (aproximado)
            'is_active': True,
            'is_default': False
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for currency_data in currencies_data:
        currency, created = Currency.objects.get_or_create(
            code=currency_data['code'],
            defaults=currency_data
        )
        
        if created:
            print(f"✅ Creada moneda: {currency.code} - {currency.name}")
            created_count += 1
        else:
            # Actualizar datos existentes
            for key, value in currency_data.items():
                setattr(currency, key, value)
            currency.save()
            print(f"🔄 Actualizada moneda: {currency.code} - {currency.name}")
            updated_count += 1
    
    print(f"\n📊 Resumen:")
    print(f"   Monedas creadas: {created_count}")
    print(f"   Monedas actualizadas: {updated_count}")
    print(f"   Total de monedas: {Currency.objects.count()}")
    
    # Mostrar monedas activas
    print(f"\n💰 Monedas activas:")
    for currency in Currency.objects.filter(is_active=True):
        default_mark = " (Por defecto)" if currency.is_default else ""
        print(f"   {currency.code} - {currency.name} - {currency.symbol} - Tasa: {currency.exchange_rate}{default_mark}")

if __name__ == '__main__':
    print("🪙 Creando monedas iniciales...")
    create_currencies()
    print("\n✅ ¡Monedas configuradas exitosamente!") 