from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from DayCareApp.DayCare.models import Profile, Parent
from DayCareApp.DayCare.forms import RegisterUserForm, LoginForm, UsernameEditForm
from django.contrib.auth.hashers import check_password


def index(request):
    return render(request, 'common/index.html')

def login_index(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    parent = get_object_or_404(Parent, profile_id=profile_id)

    request.session['profile_id'] = profile.id
    request.session['parent_id'] = parent.id

    context = {
        'profile': profile,
        'user': request.user,
        'name': parent.first_name
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

            if username not in Profile.objects.values_list('username', flat=True):
                profile = Profile(username=username, password=password)
                profile.save()

                parent = Parent(first_name=first_name, last_name=last_name, age=age, gender=gender, profile_id=profile.id)
                parent.save()

                return redirect('index')

            else:
                return render(request, 'registration/register.html')


    context = {
        'form': form

    }
    return render(request, 'registration/register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            profile = Profile.objects.get(username=username)
            if check_password(password, profile.password):

                login(request, profile, backend='django.contrib.auth.backends.ModelBackend')
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
    logout(request)
    return redirect('index')


def settings(request):
    profile_id = request.session.get('profile_id')
    parent_id = request.session.get('parent_id')

    profile = get_object_or_404(Profile, id=profile_id)
    parent = get_object_or_404(Parent, id=parent_id)

    context = {
        'profile': profile,
        'parent': parent
    }

    return render(request, 'common/settings.html', context)

def username_edit(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'GET':
        form = UsernameEditForm()

    else:
        form = UsernameEditForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            if username not in Profile.objects.values_list('username', flat=True):
                profile.username = username
                profile.save()
                return redirect('index')
            else:
                return redirect('invalid')

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'common/username_edit.html', context)

def invalid(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)

    context = {
        'profile': profile,
    }
    return render(request, 'common/invalid.html', context)





