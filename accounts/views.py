from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar al usuario después del registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente. ¡Bienvenido!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """Vista del perfil del usuario"""
    user = request.user
    # Obtener órdenes del usuario
    orders = user.order_set.all().order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)
