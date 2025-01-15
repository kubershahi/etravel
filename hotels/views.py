from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from .models import Hotel
from review.models import Review
from users.models import UserBookings
from django.contrib.auth.models import User
from .forms import RoomNumbers, Guest

from django.contrib import messages


def hotel_home(request):
    context = {}
    return render(request, 'hotel_home.html', context)


def hotel_search(request):
    try:
        l = request.GET.get('l')
        c = request.GET.get('c')
    except:
    
        l = None
        c = None

    if (l and c):
        lookup = Q(location__icontains=l) & Q(roomType__icontains=c)
        hotels = Hotel.objects.filter(lookup)

        context = {'hotels': hotels,
                   'l': l,
                   'c': c,
                   }
        template = 'hotel_result.html'
    else:
        context = {

        }
        template = 'hotel_home.html'
    return render(request, template, context)


def hotel_detail(request, hotel_id):
    if request.POST:
        hotel = get_object_or_404(Hotel, id=hotel_id)
        form = RoomNumbers(request.POST)
        if form.is_valid():
            n = form.cleaned_data.get('number')
            l = hotel.roomsLeft
            h = hotel.id
            r = l
            if (n <= l):
                return redirect(reverse('guest_detail', kwargs={'hotel_id': h, 'n': n}))
            else:
                hotel = get_object_or_404(Hotel, id=hotel_id)
                form = RoomNumbers(request.POST)
                context = {
                    'hotel': hotel,
                    'form': form,
                    'message1': "Number of rooms exceeded. Only ",
                    'message2': " rooms left.",
                    'r': l,
                }
                return render(request, 'hotel_detail.html', context)
    else:
        hotel = get_object_or_404(Hotel, id=hotel_id)
        h=hotel.hotelName
        l=hotel.location
        lookup1 = Q(hotel__icontains=h) & Q(city__icontains=l)
        reviews = Review.objects.filter(lookup1)
        form = RoomNumbers(request.POST)
        context = {
            'hotel': hotel,
            'form': form,
            'reviews':reviews,
        }
        return render(request, 'hotel_detail.html', context)


def guest_detail(request, hotel_id, n):
    if request.POST:
        hotel = get_object_or_404(Hotel, id=hotel_id)
        form = Guest(request.POST)
        if form.is_valid:
            p = hotel.price
            total = n * p
            context = {
                'hotel': hotel,
                'total': total,
                'n': n,
            }
            return render(request, 'hotelcheckout.html', context)
        else:
            context = {
                'hotel': hotel,
                'n': n,
                'form': form,
            }
            return render(request, 'guest_detail.html', context)
    else:
        hotel = get_object_or_404(Hotel, id=hotel_id)
        form = Guest(request.POST)
        context = {
            'hotel': hotel,
            'n': n,
            'form': form,
        }
        return render(request, 'guest_detail.html', context)


def hotel_payment(request, hotel_id, n):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.roomsLeft
    hotel.roomsLeft = rooms - n
    hotel.save()
    hotel = get_object_or_404(Hotel, id=hotel_id)
    currentuser = get_object_or_404(User, username=request.user.username)
    try:
        ub = UserBookings.objects.get(user=currentuser)
    except:
        ub = None
    if ub is None:
        ub = UserBookings(user=currentuser)
        ub.save()
        ub.userhotels.add(hotel)
    else:
        ub.userhotels.add(hotel)

    context = {
        'hotel': hotel,
        'n': n,
    }
    return render(request, 'hotelsuccess.html', context)
