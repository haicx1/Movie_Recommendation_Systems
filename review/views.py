from django.shortcuts import render, get_object_or_404

import utils1
from .models import Movie
from utils1 import average_rating
from django.core.paginator import Paginator


def index(request):
    return render(request, "base.html")


def movie_search(request):
    search_text = request.GET.get("search", "")
    return render(request, "search-results.html", {"search_text": search_text})


def movie_list(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        reviews = movie.rating_set.all()
        if reviews:
            movie_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            movie_rating = 0
            number_of_reviews = 0
        movie_list.append({'movie': movie,
                           'movie_rating': movie_rating,
                           'number_of_reviews': number_of_reviews})

    paginator = Paginator(movie_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'movie_list': page_obj
    }
    return render(request, 'movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.rating_set.all()
    movie_r = utils1.genre_recommendations(movie.title, k=5)
    r_list = set()
    for name in movie_r:
        r = Movie.objects.filter(title__contains=name)
        r_list.add(r)
    if reviews:
        movie_rating = average_rating([review.rating for review in reviews])
        context = {
            "movie": movie,
            "movie_rating": movie_rating,
            "reviews": reviews,
            "r_list": r_list
        }
    else:
        context = {
            "movie": movie,
            "movie_rating": None,
            "reviews": None,
            "r_list": r_list
        }
    return render(request, "movie_detail.html", context)


