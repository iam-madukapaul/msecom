from django.shortcuts import render, redirect
from .forms import CreateUserForm, CustomLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.save()
                return redirect('login')
        
        context = {
            'form': form,
        }
        return render(request, 'register_user.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CustomLoginForm()
        if request.method == 'POST':
            form = CustomLoginForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                login(request, user)
                return redirect('index')
        context = {'form': form}
        return render(request, 'login_user.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')
