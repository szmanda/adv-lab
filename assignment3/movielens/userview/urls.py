from django.urls import path
from . import views

urlpatterns = [
    path("list", views.IndexView.as_view(), name="movies_list"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="genre_detail"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="movie_detail"),
    path("movie/add", views.movie_add, name="movie_add"),
    path("movie/edit/<int:pk>", views.movie_edit, name="movie_edit"),
    path("rated", views.RatedMoviesView.as_view(), name="rated"),
    path("rating/add/<int:movie_id>", views.rating_add, name="rating_add"),
    path("rating/delete/<int:rating_id>", views.rating_delete, name="rating_delete"),
    path("comment/add/<int:movie_id>", views.comment_add, name="comment_add"),
    path("comment/delete/<int:pk>", views.comment_delete, name="comment_delete"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("search", views.search, name="search"),
    path("admin_page", views.admin_page, name="admin_page"),
    path("", views.home_page, name="home_page"),
]
