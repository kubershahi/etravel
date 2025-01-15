from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserRegisterForm, AccountUpdateForm
from django.contrib.auth.forms import UserChangeForm

from .models import GuestEmail
from django.utils.http import is_safe_url
from .forms import LoginForm

from django.contrib.auth import login, authenticate, logout

from .models import UserBookings
from flights.models import Flight
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def userprofile(request):
    context = {}
    return render(request, 'users/profile.html', context)


def edit(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = "Changes updated!"
    else:
        form = AccountUpdateForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "username": request.user.username,

            }
        )
    context['form'] = form
    return render(request, 'users/edit.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
    return render(request, 'accounts/login.html', context)


def mybookings(request):
    currentuser = get_object_or_404(User, username=request.user.username)

    try:
        flights = currentuser.userbookings.userflights.all()
    except:
        flights = None
    
    try:
        hotels = currentuser.userbookings.userhotels.all()
    except:
        hotels = None


    context = {
        'flights': flights,
        'hotels' : hotels,
    }
    return render(request, 'users/mybookings.html', context)
