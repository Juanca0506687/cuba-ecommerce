from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'symbol', 'exchange_rate', 'is_active', 'is_default']
    list_filter = ['is_active', 'is_default']
    search_fields = ['code', 'name']
    list_editable = ['exchange_rate', 'is_active', 'is_default']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'symbol')
        }),
        ('Configuración', {
            'fields': ('exchange_rate', 'is_active', 'is_default')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'category', 'currency', 'sale_price', 
        'purchase_price', 'profit_margin_display', 'stock', 
        'stock_status', 'is_active', 'is_featured'
    ]
    list_filter = [
        'category', 'currency', 'is_active', 'is_featured', 
        'created_at', 'updated_at'
    ]
    search_fields = ['name', 'code', 'description']
    list_editable = ['sale_price', 'stock', 'is_active', 'is_featured']
    readonly_fields = ['profit_margin', 'created_at', 'updated_at']
    
    actions = ['mark_as_inactive', 'mark_as_active']
    
    def mark_as_inactive(self, request, queryset):
        """Marcar productos como inactivos en lugar de eliminarlos"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} productos marcados como inactivos.')
    mark_as_inactive.short_description = "Marcar como inactivos"
    
    def mark_as_active(self, request, queryset):
        """Marcar productos como activos"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} productos marcados como activos.')
    mark_as_active.short_description = "Marcar como activos"
    
    def profit_margin_display(self, obj):
        """Muestra el margen de ganancia con formato"""
        if obj.profit_margin > 0:
            margin = f"{obj.profit_margin:.1f}"
            return format_html('<span style="color: green;">{}%</span>', margin)
        elif obj.profit_margin < 0:
            margin = f"{obj.profit_margin:.1f}"
            return format_html('<span style="color: red;">{}%</span>', margin)
        else:
            return format_html('<span style="color: gray;">0%</span>')
    profit_margin_display.short_description = "Margen"
    
    def stock_status(self, obj):
        """Muestra el estado del stock con colores"""
        if obj.is_out_of_stock:
            return format_html('<span style="color: red;">Agotado</span>')
        elif obj.is_low_stock:
            return format_html('<span style="color: orange;">Bajo</span>')
        else:
            return format_html('<span style="color: green;">OK</span>')
    stock_status.short_description = "Estado Stock"
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'code', 'category', 'description')
        }),
        ('Precios y Moneda', {
            'fields': ('currency', 'purchase_price', 'sale_price', 'profit_margin')
        }),
        ('Inventario', {
            'fields': ('stock', 'min_stock')
        }),
        ('Configuración', {
            'fields': ('image', 'is_active', 'is_featured')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    readonly_fields = ['total', 'created_at', 'updated_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'delivery_type', 'status', 
        'total_amount', 'phone', 'whatsapp_sent', 'created_at'
    ]
    list_filter = [
        'status', 'delivery_type', 'whatsapp_sent', 
        'created_at', 'updated_at'
    ]
    search_fields = ['order_number', 'user__username', 'phone', 'shipping_address']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'whatsapp_message']
    
    actions = ['mark_as_whatsapp_sent', 'mark_as_whatsapp_not_sent']
    
    def mark_as_whatsapp_sent(self, request, queryset):
        """Marcar órdenes como WhatsApp enviado"""
        updated = queryset.update(whatsapp_sent=True)
        self.message_user(request, f'{updated} órdenes marcadas como WhatsApp enviado.')
    mark_as_whatsapp_sent.short_description = "Marcar WhatsApp como enviado"
    
    def mark_as_whatsapp_not_sent(self, request, queryset):
        """Marcar órdenes como WhatsApp no enviado"""
        updated = queryset.update(whatsapp_sent=False)
        self.message_user(request, f'{updated} órdenes marcadas como WhatsApp no enviado.')
    mark_as_whatsapp_not_sent.short_description = "Marcar WhatsApp como no enviado"
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Información de Entrega', {
            'fields': ('delivery_type', 'shipping_address', 'phone', 'notes')
        }),
        ('WhatsApp', {
            'fields': ('whatsapp_sent', 'whatsapp_message'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Generar mensaje de WhatsApp al guardar"""
        if not change:  # Solo para nuevas órdenes
            obj.whatsapp_message = obj.generate_whatsapp_message()
        super().save_model(request, obj, form, change)

# Configuración del sitio admin
admin.site.site_header = "Administración de Cuba E-Commerce"
admin.site.site_title = "Cuba E-Commerce Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"
