from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal

class Currency(models.Model):
    """Modelo para manejar diferentes monedas"""
    code = models.CharField(max_length=3, unique=True, verbose_name="Código")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    symbol = models.CharField(max_length=5, verbose_name="Símbolo")
    exchange_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        default=1.0000,
        verbose_name="Tasa de Cambio (vs CUP)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    is_default = models.BooleanField(default=False, verbose_name="Por Defecto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        # Si esta moneda es por defecto, desactivar las demás
        if self.is_default:
            Currency.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls):
        """Obtiene la moneda por defecto"""
        return cls.objects.filter(is_default=True).first() or cls.objects.first()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código del Producto")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoría")
    
    # Moneda del producto
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        verbose_name="Moneda"
    )
    
    # Precios en la moneda del producto
    purchase_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Precio de Compra"
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Precio de Venta"
    )
    
    # Inventario
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Disponible")
    min_stock = models.PositiveIntegerField(default=5, verbose_name="Stock Mínimo")
    
    # Imagen del producto
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")
    
    # Estado del producto
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.code}"

    @property
    def profit_margin(self):
        """Calcula el margen de ganancia"""
        if self.purchase_price and self.purchase_price > 0 and self.sale_price:
            return ((self.sale_price - self.purchase_price) / self.purchase_price) * 100
        return 0

    @property
    def is_low_stock(self):
        """Verifica si el stock está bajo"""
        return self.stock <= self.min_stock

    @property
    def is_out_of_stock(self):
        """Verifica si el producto está agotado"""
        return self.stock == 0

    def get_price_in_currency(self, target_currency):
        """Convierte el precio de venta a otra moneda"""
        if not target_currency or target_currency == self.currency:
            return self.sale_price
        
        # Convertir usando las tasas de cambio
        cup_rate = self.currency.exchange_rate
        target_rate = target_currency.exchange_rate
        
        if cup_rate > 0 and target_rate > 0:
            # Primero convertir a CUP, luego a la moneda objetivo
            price_in_cup = self.sale_price * cup_rate
            return price_in_cup / target_rate
        
        return self.sale_price

    def get_purchase_price_in_currency(self, target_currency):
        """Convierte el precio de compra a otra moneda"""
        if not target_currency or target_currency == self.currency:
            return self.purchase_price
        
        # Convertir usando las tasas de cambio
        cup_rate = self.currency.exchange_rate
        target_rate = target_currency.exchange_rate
        
        if cup_rate > 0 and target_rate > 0:
            # Primero convertir a CUP, luego a la moneda objetivo
            price_in_cup = self.purchase_price * cup_rate
            return price_in_cup / target_rate
        
        return self.purchase_price

    def get_image_url(self):
        """Obtiene la URL de la imagen o una imagen de placeholder"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return "https://via.placeholder.com/300x200/cccccc/666666?text=Sin+Imagen"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.user.username}"

    @property
    def total(self):
        """Calcula el total del carrito"""
        return sum(item.subtotal for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        if self.product.sale_price:
            return self.quantity * self.product.sale_price
        return 0

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    DELIVERY_CHOICES = [
        ('pickup', 'Recoger en Tienda'),
        ('delivery', 'Mensajería'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Orden")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    # Información de entrega
    delivery_type = models.CharField(
        max_length=20, 
        choices=DELIVERY_CHOICES, 
        default='pickup', 
        verbose_name="Tipo de Entrega"
    )
    shipping_address = models.TextField(blank=True, verbose_name="Dirección de Envío")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Información de WhatsApp
    whatsapp_sent = models.BooleanField(default=False, verbose_name="WhatsApp Enviado")
    whatsapp_message = models.TextField(blank=True, verbose_name="Mensaje de WhatsApp")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Orden {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generar número de orden único
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
    
    def generate_whatsapp_message(self):
        """Genera el mensaje de WhatsApp para el administrador"""
        items_text = ""
        for item in self.orderitem_set.all():
            items_text += f"- {item.quantity}x {item.product.name} - {item.product.currency.symbol}{item.price}\n"
        
        if self.delivery_type == 'delivery':
            delivery_info = f"\n🚚 DIRECCIÓN DE ENVÍO:\n{self.shipping_address}"
        else:
            delivery_info = "\nRECOGER EN TIENDA"
        
        message = f"""🛒 NUEVA ORDEN - {self.order_number}

CLIENTE:
{self.user.get_full_name() or self.user.username}
Teléfono: {self.phone}

PRODUCTOS:
{items_text}TOTAL: {self.total_amount}
{delivery_info}

NOTAS:
{self.notes or 'Sin notas adicionales'}

FECHA: {self.created_at.strftime('%d/%m/%Y %H:%M')}"""
        return message

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Orden")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Item de Orden"
        verbose_name_plural = "Items de Orden"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        if self.price:
            return self.quantity * self.price
        return 0
