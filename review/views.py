from django.shortcuts import render
from review.forms import ReviewForm


def review_view(request):
    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            rating = form.cleaned_data.get('rating')
            print(rating)
            review = form.cleaned_data.get('review')
            context = {
                'rating': rating,
                'review': review,
                'form': form,
            }
            return render(request, 'flight_home.html', context)
    else:
        form = ReviewForm()
        context = {
            'form': form,
        }
        return render(request, "write.html", context)
