from django.shortcuts import render, get_object_or_404

from .models import Movie
from .utils import average_rating


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_text = request.GET.get("search", "")
    return render(request, "reviews/search-results.html", {"search_text": search_text})


def movie_list(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        reviews = movie.rating_set.all()
        if reviews:
            movie_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            movie_rating = None
            number_of_reviews = 0
        movie_list.append({'book': movie,
                          'book_rating': movie_rating,
                          'number_of_reviews': number_of_reviews})

    context = {
        'book_list': movie_list
    }
    return render(request, 'movie_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Movie, pk=pk)
    reviews = book.rating_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request, "reviews/book_detail.html", context)