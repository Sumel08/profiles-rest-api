from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import models

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html')

def create_event(request):
    return render(request, 'create_event.html')

@login_required
def dashboard(request):

    return render(request, 'dashboard.html', {'user': request.user})

@login_required
def logout(request):
    django_logout(request)
    #return render(request, 'login.html', {})
    return redirect('/login')
