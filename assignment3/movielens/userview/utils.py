from django.db.models import Count
from django.db import models
from .models import Movie, Rating
import datetime


# finds similar movies by counting the number of common genres
def get_similar_movies(movie_id):
    given_movie = Movie.objects.get(id=movie_id)
    given_movie_genres = given_movie.genres.all()
    
    similar_movies = Movie.objects.exclude(id=movie_id).annotate(
        common_genre_count=Count('genres', filter=models.Q(genres__in=given_movie_genres))
    ).filter(common_genre_count__gte=1).order_by('-common_genre_count')

    return similar_movies

def get_recently_most_liked_movies(cutoff_date = datetime.date.today()):
    recent_ratings = Rating.objects.filter(value__gte=3) # TODO: Add timestamp__gte=cutoff_date

    liked_movies = Movie.objects.filter(rating__in=recent_ratings).annotate(
        positive_rating_count=Count('rating', output_field=models.IntegerField())
    ).order_by('-positive_rating_count')[:10]
    
    for movie in liked_movies:
        print(movie.title, movie.positive_rating_count, type(movie.positive_rating_count))

    return liked_movies