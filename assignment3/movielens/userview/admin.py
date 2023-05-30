from django.contrib import admin

# Register your models here.

from . models import Rating, Genre, Movie, Comment

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Comment)