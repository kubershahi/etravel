from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from .forms import Number, Passenger
from django.contrib import messages

from users.models import UserBookings
from .models import Flight
from django.contrib.auth.models import User


def flight_home(request):
    context = {}
    return render(request, 'flight_home.html', context)


def flight_search(request):
    try:
        q = request.GET.get('q')
        r = request.GET.get('r')
        c = request.GET.get('c')
        d = request.GET.get('d')
    except:
        q = None
        r = None
        c = None
        d = None

    if (q and r and c and d):

        lookup = Q(sourceLocation__icontains=q) & Q(destinationLocation__icontains=r) & Q(classtype__icontains=c) & Q(departureDate__icontains=d)
        flights = Flight.objects.filter(lookup)
        context = {'flights': flights,
                   'q': q,
                   'r': r,
                   'c': c,
                   'd': d,
                   }
        template = 'flight_result.html'
    else:
        context = {}
        template = 'flight_home.html'
    return render(request, template, context)


def flight_detail(request, flight_id):
    if request.POST:
        flight = get_object_or_404(Flight, id=flight_id)
        form = Number(request.POST)
        if form.is_valid():
            n = form.cleaned_data.get('number')
            l = flight.numSeatsRemaining
            f = flight.id
            if (n <= l):
                return redirect(reverse('passenger_detail', kwargs={'flight_id': f, 'n': n}))
            else:
                flight = get_object_or_404(Flight, id=flight_id)
                form = Number(request.POST)
                context = {
                    'flight': flight,
                    'form': form,
                    'message1': "Number of seats exceeded. Only ",
                    'message2': " seats left.",
                    'r': l,
                }
                return render(request, 'flight_detail.html', context)
    else:
        flight = get_object_or_404(Flight, id=flight_id)
        form = Number(request.POST)
        context = {
            'flight': flight,
            'form': form,
        }
        return render(request, 'flight_detail.html', context)


def passenger_detail(request, flight_id, n):
    if request.POST:
        flight = get_object_or_404(Flight, id=flight_id)
        form = Passenger(request.POST)
        if form.is_valid:
            p = flight.price
            total = n * p
            context = {
                'flight': flight,
                'total': total,
                'n': n,
            }
            return render(request, 'checkout.html', context)
        else:
            context = {
                'flight': flight,
                'n': n,
                'r': range(n),
                'i': 1,
                'form': form,
            }
            return render(request, 'passenger_detail.html', context)
    else:
        flight = get_object_or_404(Flight, id=flight_id)
        form = Passenger(request.POST)
        context = {
            'flight': flight,
            'n': n,
            'r': range(n),
            'i': 1,
            'form': form,
        }
        return render(request, 'passenger_detail.html', context)


def flight_payment(request, flight_id, n):
    flight = get_object_or_404(Flight, id=flight_id)
    seats = flight.numSeatsRemaining
    flight.numSeatsRemaining = seats - n
    flight.save()
    flight = get_object_or_404(Flight, id=flight_id)
    currentuser = get_object_or_404(User, username=request.user.username)
    try:
        ub = UserBookings.objects.get(user=currentuser)
    except:
        ub = None
    if ub is None:
        ub = UserBookings(user=currentuser)
        ub.save()
        ub.userflights.add(flight)
    else:
        ub.userflights.add(flight)

    context = {
        'flight': flight,
        'n': n,
    }
    return render(request, 'success.html', context)


def flight_view(request):
    queryset = Flight.objects.all()  # list of objects
    # pages = pagination(request,queryset,100)
    context = {
        'items': queryset,
        # 'page_range': pages[1]
    }
    return render(request, "flight_list.html", context)
