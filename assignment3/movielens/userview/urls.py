from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="movies_list"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="genre_detail"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="movie_detail"),
    path("rated", views.RatedMoviesView.as_view(), name="rated"),
    path("rating/add/<int:movie_id>", views.rating_add, name="rating_add"),
    path("rating/delete/<int:rating_id>", views.rating_delete, name="rating_delete"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
]
