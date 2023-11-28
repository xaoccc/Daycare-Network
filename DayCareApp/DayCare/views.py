
from django.shortcuts import render, redirect
from DayCareApp.DayCare.models import Profile, Parent
from DayCareApp.DayCare.forms import RegisterUserForm

# Create your views here.


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
    return render(request, 'users/register.html', context)


def login(request):
    # create login form, validate forms, create context
    return render(request, 'users/login.html')


