from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . import forms


# Create your views here.
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('/', {'message': message})
            else:
                message = 'Identifiants invalides.'
    return render(
            request, 'Authenticate/login_page.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    message = ''
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                user = User.objects.create_user(
                    username=form.data['username'],
                    password=form.data['password'],
                )
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('/',{'message': message})
            else:
                message = 'Les mots de passe ne correspondent pas.'
    return render(request,'Authenticate/signup_page.html', context={'form': form, 'message': message})


def logout_page(request):
    logout(request)
    message = f'vous etes deconnecte'
    return redirect('/', {'message': message})