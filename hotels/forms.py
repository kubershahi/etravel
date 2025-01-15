from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class RoomNumbers(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=50)


def validate_phone(self, value):
    if len(value) != 10:
        raise ValidationError(
            _('Must be a valid Phone Number.'),
            params={'value': value},
        )


class Guest(forms.Form):
    firstname = forms.CharField(required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastname = forms.CharField(required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    nationality = forms.CharField(required=True, label='Nationality', widget=forms.TextInput(attrs={'placeholder': 'Nationality'}))
    age = forms.IntegerField(required=True, label='Age', widget=forms.NumberInput(attrs={'placeholder': 'Age'}))
    phonenumber = forms.IntegerField(validators=[MinValueValidator(10000000000), MaxValueValidator(9999999999)], required=True, label='Phone Number')
    checkin = forms.DateField(required=True, label='Check In Date', widget=forms.SelectDateWidget)
