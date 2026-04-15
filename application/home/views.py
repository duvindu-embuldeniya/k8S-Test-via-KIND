from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from . forms import UserRegistrationForm
from django.contrib import messages

from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError



def health(request):
    for db_name in connections:
        try:
            connections[db_name].cursor()
        except OperationalError:
            return HttpResponse("status: db down", status=503)

    return HttpResponse("status: ok", status=200)

def startup(request):
    return HttpResponse("started", status=200)


def readiness(request):
    for db_name in connections:
        try:
            connections[db_name].cursor()
        except OperationalError:
            return HttpResponse("db down", status=503)

    return HttpResponse("ready", status=200)


def liveness(request):
    return HttpResponse("alive", status=200)


def home(request):
    return render(request, 'home/index.html')



def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()

            messages.success(request, "Account Created Successfully!")
            auth.login(request, new_user)
            return redirect('home')

    context = {'form':form}
    return render(request, 'home/register.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You've Already Loged-In!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully Loged-In!")
            return redirect('home')
        else:
            messages.error(request, "User doesn't Exist!")
            return redirect('login')
    return render(request, 'home/login.html')


def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You haven't Loged-In!")
        return redirect('home')
    auth.logout(request)
    messages.success(request,"Successfully Loged-out!")
    return redirect('home')