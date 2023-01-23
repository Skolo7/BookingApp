from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == "POST": # warunek zostanie spełniony jeśli user wyśle formularz
        form = UserCreationForm() # zatem tworzy się obiekt UserCreationForm
        # sprawdzenie czy formularz jest poprawnie wprowadzony przez usera
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account's been created for {username}")
            return redirect('index')
    else:
        form = UserCreationForm()


    return render(request, 'users/register.html', {'form': form})

def login(request):
    form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})