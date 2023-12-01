from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from DayCareApp.DayCare.models import Profile, Parent
from DayCareApp.DayCare.forms import RegisterUserForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    return render(request, 'common/index.html')

def login_index(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    context = {
        'profile': profile,
    }

    return render(request, 'common/index.html', context)

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

        try:
            profile = Profile.objects.get(username=username)

            if check_password(password, profile.password):

                profile.is_authenticated = True
                profile.save()

                return redirect('login_index', profile_id=profile.id)

            else:
                form = LoginForm()
                context = {
                    'form': form,
                    'error_message': 'Incorrect password. Try again.',
                }
                return render(request, 'registration/login.html', context)

        except Profile.DoesNotExist:
            form = LoginForm()
            context = {
                'form': form,
                'error_message': 'No such user name. Please try again.',
            }
            return render(request, 'registration/login.html', context)


    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)


def log_out(request):
    user_id = request.session.get('id')

    if user_id:
        try:
            profile = Profile.objects.get(id=user_id)
            profile.is_authenticated = False
            profile.save()

        except Profile.DoesNotExist:
            pass
    request.session.clear()
    return redirect('index')






