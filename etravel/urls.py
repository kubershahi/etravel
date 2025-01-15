from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

from flights.views import (
    flight_home,
    flight_search,
    flight_detail,
    passenger_detail,
    flight_payment,
)

from hotels.views import (
    hotel_home,
    hotel_search,
    hotel_detail,
    guest_detail,
    hotel_payment,
)

from users.views import (
    mybookings,
)

from review.views import (
    review_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # flight urls
    path('', flight_home, name='home'),  # Homepage
    path('s/', flight_search, name='flight_search'),
    path('flightdetail/<int:flight_id>/', flight_detail, name='flight_detail'),
    path('passengerdetail/<int:flight_id>/<int:n>/', passenger_detail, name='passenger_detail'),
    path('flightpayment/<int:flight_id>/<int:n>/', flight_payment, name='flight_payment'),


    # hotel urls
    path('hotel/', hotel_home, name='hotels'),
    path('hs/', hotel_search, name = 'hotel_search'),
    path('hoteldetail/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('guestdetail/<int:hotel_id>/<int:n>/', guest_detail, name='guest_detail'),
    path('hotelpayment/<int:hotel_id>/<int:n>/', hotel_payment, name='hotel_payment'),

    # review urls
    path('reviews/', review_view, name='review'),

    # user urls
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.userprofile, name='profile'),
    path('edit/', user_views.edit, name='edit'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('mybookings/', mybookings, name="mybookings"),

    # password change/reset urls (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    # password change urls
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    # password reset urls
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
