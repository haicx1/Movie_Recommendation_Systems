from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    paginator = Paginator(movies, 25)
    page_num = request.GET.get("page")
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'page_obj': page_obj
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
