from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def main(request):
    return render(request, 'admin_interface/main.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт')
                return redirect(request.GET['next'] if 'next' in request.GET else 'main')
            else:
                messages.error(request, 'Неверный логин или пароль')
        except:
            messages.error(request, 'Пользователь с таким логином не найден')
    
    return render(request, 'admin_interface/login.html')