from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("Post correct")
        if form.is_valid():
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']
            messages.success(request, 'Account was Created for ')
            print("Created account!")
            user = User.objects.create_user(username=username,
                                            password=password, email=email)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('index')


    context = {"form": UserLoginForm}
    return render(request, 'users/login.html', context)