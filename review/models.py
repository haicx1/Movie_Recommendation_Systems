from django.db import models


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.TextField()
    genres = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.genres})"

    class Meta:
        managed = True
        db_table = 'movie'


class UserMovie(models.Model):
    user_id = models.AutoField(primary_key=True)
    gender = models.TextField()
    age = models.IntegerField()
    occupation = models.IntegerField()
    zipcode = models.TextField()
    age_desc = models.TextField(blank=True, null=True)
    occ_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_movie'


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserMovie, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rating'
