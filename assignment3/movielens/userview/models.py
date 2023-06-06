from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=1000)
    year = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre)
    director = models.CharField(max_length=200, default='')
    average_rating = models.FloatField(default=0)
    imdbLink = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    image = models.ForeignKey('MovieImage', on_delete=models.SET_NULL, null=True, blank=True, related_name='movies_with_front_image')

    
class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return f'{self.image.name} ({self.pk})'

class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: Add timestamp = models.DateTimeField(auto_now_add=True) # required for get_recently_most_liked_movies
    
class Comment(models.Model):
    text = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.IntegerField(default=0)