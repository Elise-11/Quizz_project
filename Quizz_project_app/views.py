from django.shortcuts import render, redirect
from Quizz_project_app.forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import hashlib


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created for ' + user.get_username())

            return redirect('login')

    context = {'form': form}
    return render(request, 'Registration/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def explo_image(request):
    return render(request, 'Exploration/image_exploration.html')

def explo_data(request):
    return render(request, 'Exploration/list_exploration.html')

def explo(request):
    return render(request, 'Exploration/home_exploration.html')






