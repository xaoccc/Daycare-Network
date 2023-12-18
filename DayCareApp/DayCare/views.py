from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from DayCareApp.DayCare.models import Profile, Parent
from DayCareApp.DayCare.forms import RegisterUserForm, LoginForm, UsernameEditForm, PasswordEditForm
from django.contrib.auth.hashers import check_password, make_password


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


def login_index(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    parent = get_object_or_404(Parent, profile_id=profile_id)

    request.session['profile_id'] = profile.id
    request.session['parent_id'] = parent.id

    context = {
        'profile': profile,
        'profile_id': profile_id,
        'user': request.user,
        'name': parent.first_name
    }

    return render(request, 'common/index.html', context)


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
                Profile.objects.filter(username=profile.username).update(username=username)
                messages.success(request, 'Username updated successfully.')
                return redirect('login_index', profile_id=profile.id)
            else:
                messages.error(request, "Username already exists!")

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'common/username_edit.html', context)


def password_edit(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'GET':
        form = PasswordEditForm()

    else:
        form = PasswordEditForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            Profile.objects.filter(password=profile.password).update(password=make_password(password))

            messages.success(request, 'Password updated successfully.')
            return redirect('login_index', profile_id=profile.id)

        messages.error(request, 'Your password must be at least 8 characters lond and must contain digits and letters, at least one capital and one small letter.')

        context = {
            'profile': profile,
            'form': form,
        }

        return render(request, 'common/password_edit.html', context)

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'common/password_edit.html', context)

def user_data(request):
    profiles = Profile.objects.all()
    parents = Parent.objects.all()


    context = {
        'profiles': profiles,
        'parents': parents
    }

    return render(request, 'common/all_users.html', context)









