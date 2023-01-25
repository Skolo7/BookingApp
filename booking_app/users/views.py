from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == "POST": # formularz
        form = UserRegistrationForm(request.POST)
        # sprawdzenie czy formularz jest poprawnie wprowadzony przez usera
        if form.is_valid():
            form.save()
            messages.success(request, f"Account has been created")
            return redirect('index')
    else:
        form = UserRegistrationForm()


    return render(request, 'users/register.html', {'form': form})

def login(request):
    form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})