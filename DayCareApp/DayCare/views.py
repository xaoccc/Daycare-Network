from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from DayCareApp.DayCare.models import Profile, Parent
from DayCareApp.DayCare.forms import RegisterUserForm, LoginForm


def index(request):
    return render(request, 'common/index.html')

def register(request):
    if request.method == 'GET':
        form = RegisterUserForm()

    else:
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']

            profile = Profile(username=username, password=password)
            profile.save()

            parent = Parent(first_name=first_name, last_name=last_name, age=age, gender=gender)
            parent.save()

            return redirect('index')

    context = {
        'form': form

    }
    return render(request, 'registration/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # to repair authentication and hash password
        user = Profile.objects.get(username=username, password=password)

        if user is not None:
            return redirect('index')
        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)





