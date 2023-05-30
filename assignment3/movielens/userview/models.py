from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)
    average_rating = models.FloatField(default=0)
    imdb_reference = models.IntegerField(default=0)
    

class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Comment(models.Model):
    text = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)