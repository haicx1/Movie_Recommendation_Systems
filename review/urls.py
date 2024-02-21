from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.movie_list, name='book_list'),
    path('books/<int:pk>/', views.movie_detail, name='book_detail')
]
