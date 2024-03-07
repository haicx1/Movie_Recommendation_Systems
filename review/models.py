from django.db import models


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.TextField()
    genres = models.TextField()

    class Meta:
        db_table = 'movie'


class Rating(models.Model):
    user = models.ForeignKey('UserMovie', models.CASCADE, blank=True, null=True)
    movie = models.ForeignKey(Movie, models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'rating'


class UserMovie(models.Model):
    user_id = models.AutoField(primary_key=True)
    gender = models.TextField()
    age = models.IntegerField()
    occupation = models.IntegerField()
    zipcode = models.TextField()
    age_desc = models.TextField(blank=True, null=True)
    occ_desc = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_movie'