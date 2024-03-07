from django.shortcuts import render, get_object_or_404

import utils1
from .models import Movie
from utils1 import average_rating


def index(request):
    return render(request, "base.html")


def movie_search(request):
    if request.method == "POST":
        search_text = request.POST["search_text"]
    movies = Movie.objects.filter(title__icontains=search_text)
    context = {"movies": movies,
               "search_text": search_text}
    return render(request, "search-results.html", context)


def movie_list(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        movie_list.append({'movie': movie})
    context = {
        'movie_list': movie_list
    }
    return render(request, 'movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie_r = utils1.genre_recommendations(movie.title, k=5)
    r_list = set()
    for name in movie_r:
        r = Movie.objects.filter(title__icontains=name)
        r_list.add(r)
    context = {
        "movie": movie,
        "r_list": r_list
    }
    return render(request, "movie_detail.html", context)
