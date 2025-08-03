#!/usr/bin/env python
"""
Script para crear datos de ejemplo en el sistema Cuba E-Commerce
Ejecutar con: python create_sample_data.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuba_ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product

def create_sample_data():
    print("🌱 Creando datos de ejemplo para Cuba E-Commerce...")
    
    # Crear categorías
    categories_data = [
        {
            'name': 'Electrónicos',
            'description': 'Productos electrónicos y tecnología de última generación'
        },
        {
            'name': 'Ropa y Accesorios',
            'description': 'Moda y accesorios para toda la familia'
        },
        {
            'name': 'Hogar y Jardín',
            'description': 'Productos para el hogar y jardinería'
        },
        {
            'name': 'Deportes',
            'description': 'Equipamiento y ropa deportiva'
        },
        {
            'name': 'Libros y Educación',
            'description': 'Libros, material educativo y papelería'
        },
        {
            'name': 'Alimentos',
            'description': 'Productos alimenticios y bebidas'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"✅ Categoría creada: {category.name}")
    
    # Crear productos
    products_data = [
        {
            'name': 'Smartphone Samsung Galaxy A54',
            'description': 'Teléfono inteligente con cámara de 50MP, pantalla de 6.4" y batería de 5000mAh',
            'code': 'SM-A545',
            'category': categories[0],
            'purchase_price': 15000.00,
            'sale_price': 18000.00,
            'stock': 25,
            'is_featured': True
        },
        {
            'name': 'Laptop HP Pavilion 15',
            'description': 'Laptop con procesador Intel i5, 8GB RAM, 512GB SSD y Windows 11',
            'code': 'HP-PAV-15',
            'category': categories[0],
            'purchase_price': 45000.00,
            'sale_price': 55000.00,
            'stock': 10,
            'is_featured': True
        },
        {
            'name': 'Camiseta Polo Clásica',
            'description': 'Camiseta polo de algodón 100%, disponible en varios colores',
            'code': 'POLO-001',
            'category': categories[1],
            'purchase_price': 800.00,
            'sale_price': 1200.00,
            'stock': 50,
            'is_featured': False
        },
        {
            'name': 'Zapatillas Deportivas Nike Air Max',
            'description': 'Zapatillas deportivas con tecnología Air Max, ideales para running',
            'code': 'NIKE-AM-001',
            'category': categories[3],
            'purchase_price': 2500.00,
            'sale_price': 3500.00,
            'stock': 30,
            'is_featured': True
        },
        {
            'name': 'Set de Ollas de Cocina',
            'description': 'Set completo de ollas de acero inoxidable, 6 piezas',
            'code': 'OLLAS-001',
            'category': categories[2],
            'purchase_price': 3000.00,
            'sale_price': 4500.00,
            'stock': 15,
            'is_featured': False
        },
        {
            'name': 'Libro "El Principito"',
            'description': 'Clásico de la literatura universal, edición especial con ilustraciones',
            'code': 'LIB-001',
            'category': categories[4],
            'purchase_price': 150.00,
            'sale_price': 250.00,
            'stock': 100,
            'is_featured': False
        },
        {
            'name': 'Café Cubano Premium',
            'description': 'Café 100% cubano, grano entero, 500g',
            'code': 'CAFE-001',
            'category': categories[5],
            'purchase_price': 200.00,
            'sale_price': 350.00,
            'stock': 75,
            'is_featured': True
        },
        {
            'name': 'Tablet Samsung Galaxy Tab A8',
            'description': 'Tablet con pantalla de 10.5", 4GB RAM, 64GB almacenamiento',
            'code': 'TAB-A8',
            'category': categories[0],
            'purchase_price': 12000.00,
            'sale_price': 15000.00,
            'stock': 20,
            'is_featured': False
        },
        {
            'name': 'Jeans Levi\'s 501',
            'description': 'Jeans clásicos de alta calidad, corte recto',
            'code': 'LEVI-501',
            'category': categories[1],
            'purchase_price': 1200.00,
            'sale_price': 1800.00,
            'stock': 40,
            'is_featured': False
        },
        {
            'name': 'Balón de Fútbol Oficial',
            'description': 'Balón de fútbol profesional, tamaño 5, material sintético',
            'code': 'BALON-001',
            'category': categories[3],
            'purchase_price': 800.00,
            'sale_price': 1200.00,
            'stock': 60,
            'is_featured': False
        },
        {
            'name': 'Mochila Escolar con Ruedas',
            'description': 'Mochila escolar con ruedas, múltiples compartimentos',
            'code': 'MOCH-001',
            'category': categories[4],
            'purchase_price': 600.00,
            'sale_price': 900.00,
            'stock': 35,
            'is_featured': False
        },
        {
            'name': 'Aceite de Oliva Extra Virgen',
            'description': 'Aceite de oliva extra virgen, 500ml, importado',
            'code': 'ACEITE-001',
            'category': categories[5],
            'purchase_price': 400.00,
            'sale_price': 600.00,
            'stock': 45,
            'is_featured': False
        }
    ]
    
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            code=prod_data['code'],
            defaults={
                'name': prod_data['name'],
                'description': prod_data['description'],
                'category': prod_data['category'],
                'purchase_price': prod_data['purchase_price'],
                'sale_price': prod_data['sale_price'],
                'stock': prod_data['stock'],
                'is_featured': prod_data['is_featured']
            }
        )
        if created:
            print(f"✅ Producto creado: {product.name} - {product.sale_price} CUP")
    
    print("\n🎉 ¡Datos de ejemplo creados exitosamente!")
    print("\n📊 Resumen:")
    print(f"   • Categorías: {Category.objects.count()}")
    print(f"   • Productos: {Product.objects.count()}")
    print(f"   • Productos destacados: {Product.objects.filter(is_featured=True).count()}")
    print(f"   • Productos activos: {Product.objects.filter(is_active=True).count()}")
    
    print("\n🔗 Enlaces útiles:")
    print("   • Sitio web: http://127.0.0.1:8000/")
    print("   • Panel de administración: http://127.0.0.1:8000/admin/")
    print("   • Usuario admin: admin")
    print("   • Contraseña admin: admin123")

if __name__ == '__main__':
    create_sample_data() 