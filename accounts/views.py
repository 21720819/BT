from django.shortcuts import render,redirect
from django.contrib import auth
from .forms import UserSignupform, UserLoginform
from .models import User

def home(request):
    return render(request,'home.html')


def signup(request):
    if request.method == "POST":
        form = UserSignupform(request.POST)
        if request.POST["password"]==request.POST["password2"]:
            user = User.objects.create_user(
                email= request.POST['email'], password=request.POST['password'] ,username = request.POST['username']
            )
            auth.login(request,user)
            return redirect('home')
        return render(request,'accounts/signup.html',{'form':form})
    else:
        form = UserSignupform()
    return render(request, 'accounts/signup.html',{'form':form})

def login(request):
    if request.method =="POST":
        form = UserLoginform(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email = email, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            render(request, 'accounts/bad_login.html',{'form':form})
    else:
        form = UserLoginform()
        return render(request, 'accounts/login.html',{'form':form})

def logout(request):
    auth.logout(request)
    return redirect('home')
