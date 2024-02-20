from django.db import models


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True, blank=True, null=True)
    title = models.TextField()
    genres = models.TextField()

    class Meta:
        managed = False
        db_table = 'movie'


class Rating(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rating'


class User(models.Model):
    user_id = models.AutoField(primary_key=True, blank=True, null=True)
    gender = models.TextField()
    age = models.IntegerField()
    occupation = models.IntegerField()
    zipcode = models.TextField()
    age_desc = models.TextField(blank=True, null=True)
    occ_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
