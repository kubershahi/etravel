from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from review.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = forms.CharField()

    class Meta:
        model = Review
        fields = ('city', 'hotel', 'rating', 'review',)
