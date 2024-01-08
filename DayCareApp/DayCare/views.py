from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from DayCareApp.DayCare.models import Profile, Parent, Offers, Location, Child
from DayCareApp.DayCare.forms import RegisterUserForm, LoginForm, UsernameEditForm, PasswordEditForm, RegisterOfferForm, RegisterLocationForm, RegisterChildForm
from django.contrib.auth.hashers import check_password, make_password
from psycopg2._psycopg import Decimal


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
                context = {
                    'form': form
                }
                return render(request, 'registration/register.html', context)

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
                request.session['profile_id'] = profile.id
                return redirect('login_index')

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


def login_index(request):
    profile_id = request.session.get('profile_id')

    profile = get_object_or_404(Profile, id=profile_id)
    parent = get_object_or_404(Parent, profile_id=profile_id)

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
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)

    profiles = Profile.objects.all()
    parents = Parent.objects.all()
    context = {
        'profile': profile,
        'profiles': profiles,
        'parents': parents
    }

    return render(request, 'common/all_users.html', context)


def services(request):
    profiles = Profile.objects.all()
    parents = Parent.objects.all()

    context = {
        'profiles': profiles,
        'parents': parents
    }
    return render(request, 'common/services.html', context)


def offers(request):
    profiles = Profile.objects.all()
    parents = Parent.objects.all()

    context = {
        'profiles': profiles,
        'parents': parents
    }
    return render(request, 'common/offers.html', context)


def register_offer(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    parent = Parent.objects.get(profile_id=profile_id)

    if request.method == 'GET':
        offer_form = RegisterOfferForm()
        location_form = RegisterLocationForm()

    else:
        offer_form = RegisterOfferForm(request.POST)
        location_form = RegisterLocationForm(request.POST)

        if offer_form.is_valid() and location_form.is_valid():
            min_rating = offer_form.cleaned_data['min_rating']
            price_per_hour = offer_form.cleaned_data['price_per_hour']

            location = location_form.save()
            offer = Offers(
                min_rating=min_rating,
                price_per_hour=price_per_hour,
                location_ptr_id=location.id,
                location_name=location.location_name,
                hospitals=location.hospitals,
                schools=location.schools
            )
            offer.save()

            parent.parent_offer_id = offer.id
            parent.save()

            return redirect('login_index')

    context = {
        'profile': profile,
        'offer_form': offer_form,
        'location_form': location_form
    }
    return render(request, 'registration/register_offer.html', context)


def delete_user(request):
    try:
        profile_id = request.session.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        parent = Parent.objects.get(profile_id=profile_id)
        profile.delete()
        parent.delete()
        return render(request, 'common/index.html')
    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist
        return render(request, 'common/error.html', {'error_message': 'Profile not found'})
    except Parent.DoesNotExist:
        # Handle the case where the parent does not exist
        return render(request, 'common/error.html', {'error_message': 'Parent not found'})
    except Exception as e:
        # Handle other exceptions (e.g., database errors) more gracefully
        return render(request, 'common/error.html', {'error_message': str(e)})


def find_offers(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    parent = Parent.objects.get(profile_id=profile_id)

    if not parent.parent_offer:
        context = {
            'profile': profile,
            'profile_id': profile_id,
            'error_message': 'Please create a job offer first. We have no min rating criteria, so we can display the available job offers.'
        }

        return render(request, 'common/error.html', context)

    # find all valid job offers, including parent and location info
    available_job_offers = Offers.objects.select_related('parent').filter(
        parent__rating__gte=parent.parent_offer.min_rating).exclude(parent__id=parent.id)

    context = {
        'profile': profile,
        'available_job_offers': available_job_offers,
        'profile_id': profile_id
    }
    return render(request, 'common/offers.html', context)

def register_child(request):
    profile_id = request.session.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    parent = Parent.objects.get(profile_id=profile_id)

    if request.method == 'GET':
        form = RegisterChildForm()

    else:
        form = RegisterChildForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            has_special_needs = form.cleaned_data['has_special_needs']

            child = Child(first_name=first_name, last_name=last_name, age=age, has_special_needs=has_special_needs, parent=parent)
            child.save()

            return redirect('login_index')

    context = {
        'profile': profile,
        'form': form
    }

    return render(request, 'registration/register_child.html', context)











