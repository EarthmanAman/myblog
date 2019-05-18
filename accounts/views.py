from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from .forms import UserRegisterForm


def user_register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            new_user.username = email
            new_user.set_password(password)
            new_user.save()
            username = form.cleaned_data['username']
            userIn = authenticate(username=username, password=password)
            if userIn:
                login(request, userIn)
                return redirect("/")
    return render(request, './register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        userIn = authenticate(username=username, password=password)
        if userIn:
            login(request, userIn)
            return redirect("/")
    return render(request, './login.html')


def logout_user(request):
    logout(request)
    return redirect("/")

