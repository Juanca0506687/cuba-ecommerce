from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from urllib.parse import quote
from django.conf import settings

def home(request):
    """Vista principal de la tienda"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """Lista de productos con filtros"""
    products = Product.objects.filter(is_active=True)
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'name')
    
    # Filtro por categoría
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Búsqueda
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(code__icontains=search_query)
        )
    
    # Ordenamiento
    if sort_by == 'price_low':
        products = products.order_by('sale_price')
    elif sort_by == 'price_high':
        products = products.order_by('-sale_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Paginación
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, product_id):
    """Detalle de un producto"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock:
            messages.error(request, 'No hay suficiente stock disponible.')
            return redirect('product_detail', product_id=product_id)
        
        # Obtener o crear carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Obtener o crear item del carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} agregado al carrito.')
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def cart(request):
    """Vista del carrito"""
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()
    except Cart.DoesNotExist:
        cart = None
        items = []
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'store/cart.html', context)

@login_required
def cart_count(request):
    """Vista para obtener el contador del carrito (AJAX)"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.cartitem_set.count()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})

@login_required
def update_cart_item(request, item_id):
    """Actualizar cantidad en el carrito"""
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 0))
        
        if quantity <= 0:
            item.delete()
            messages.success(request, 'Producto removido del carrito.')
        elif quantity > item.product.stock:
            messages.error(request, 'No hay suficiente stock disponible.')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Carrito actualizado.')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    """Remover producto del carrito"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Producto removido del carrito.')
    return redirect('cart')

@login_required
def checkout(request):
    """Procesa el checkout y crea la orden"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        delivery_type = request.POST.get('delivery_type', 'pickup')
        shipping_address = request.POST.get('shipping_address', '')
        phone = request.POST.get('phone', '')
        notes = request.POST.get('notes', '')
        
        # Validaciones
        if not phone:
            messages.error(request, 'El teléfono es obligatorio.')
            return redirect('cart')
        
        if delivery_type == 'delivery' and not shipping_address:
            messages.error(request, 'La dirección de envío es obligatoria para mensajería.')
            return redirect('cart')
        
        try:
            # Crear la orden
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total,
                delivery_type=delivery_type,
                shipping_address=shipping_address,
                phone=phone,
                notes=notes
            )
            
            # Crear los items de la orden
            for item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.sale_price
                )
                
                # Actualizar stock
                item.product.stock -= item.quantity
                item.product.save()
            
            # Generar mensaje de WhatsApp
            whatsapp_message = order.generate_whatsapp_message()
            order.whatsapp_message = whatsapp_message
            order.save()
            
            # Limpiar el carrito
            cart.delete()
            
            # Crear URL de WhatsApp usando la configuración
            whatsapp_number = getattr(settings, 'WHATSAPP_NUMBER', '5351234567')
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={quote(whatsapp_message)}"
            
            messages.success(request, f'¡Orden {order.order_number} creada exitosamente!')
            return render(request, 'store/order_success.html', {
                'order': order,
                'whatsapp_url': whatsapp_url
            })
            
        except Exception as e:
            messages.error(request, f'Error al procesar la orden: {str(e)}')
            return redirect('cart')
    
    return render(request, 'store/checkout.html', {
        'cart': cart
    })

@login_required
def order_list(request):
    """Lista de órdenes del usuario"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_list.html', context)

@login_required
def order_detail(request, order_id):
    """Detalle de una orden"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)
