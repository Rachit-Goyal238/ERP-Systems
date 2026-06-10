from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                'dashboard_v3'
            )

        else:

            messages.error(

                request,

                'Invalid username or password'

            )

    return render(

        request,

        'accounts/login.html'
    )

def register_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match'
            )

            return redirect(
                'register'
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect(
                'register'
            )

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )

        group, created = (
            Group.objects.get_or_create(
                name='Employee'
            )
        )

        user.groups.add(
            group
        )

        messages.success(
            request,
            'Account created successfully'
        )

        return redirect(
            'login'
        )

    return render(
        request,
        'accounts/register.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')