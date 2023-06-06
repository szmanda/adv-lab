from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Movie, Genre, Rating, Comment, MovieImage
from .forms import NewUserForm, RatingForm, MovieForm, CommentForm, MovieImageForm



def index(request: HttpRequest):
    movies = Movie.objects.order_by('-title')
    template = loader.get_template('userview/movies_list.html')
    context = {
        'movies': movies
    }
    return HttpResponse(template.render(context, request))

def view_movie(request: HttpRequest, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.genres = movie.genres.all()
    template = loader.get_template('userview/movie_detail.html')
    context = {
        'movie': movie
    }
    return HttpResponse(template.render(context, request))

def view_genre(request: HttpRequest, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    template = loader.get_template('userview/genre_detail.html')
    context = {
        'genre': genre
    }
    return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'userview/movies_list.html'
    context_object_name = 'movies'
    def get_queryset(self):
        return Movie.objects.order_by('-title')
    
class MovieView(generic.DetailView):
    model = Movie
    template_name = 'userview/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = self.object.genres.all()
        context['comments'] = Comment.objects.filter(movie=self.object)
        return context

class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre_detail.html'

class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'userview/movies_list.html'
    context_object_name = 'movies'
    def get_queryset(self):
        return Movie.objects.order_by('-title')
    
class RatedMoviesView(LoginRequiredMixin, generic.ListView):
    model = Movie
    template_name = 'userview/rated_movies_list.html'
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        ratings = Rating.objects.filter(user=user)
        movie_ids = ratings.values_list('movie_id', flat=True)
        queryset = Movie.objects.filter(id__in=movie_ids)
        return queryset
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for movie in context['movies']:
            movie.rating = Rating.objects.get(movie=movie, user=self.request.user)
        return context

from django.db.models import Avg
def rating_add(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        if request.method == 'POST':
            form = RatingForm(request.POST)
            if form.is_valid():
                rating_value = form.cleaned_data['value']
                user = request.user
                rating, created = Rating.objects.get_or_create(movie=movie, user=user, defaults={'value': rating_value})
                if not created:
                    rating.value = rating_value
                    rating.save()
                messages.success(request, f'Your rating for {movie.title} has been saved.')
                # updating average rating
                movie_ratings = Rating.objects.filter(movie=movie)
                movie.average_rating = movie_ratings.aggregate(Avg('value'))['value__avg']
                movie.save()
                return redirect('rated')
        else:
            form = RatingForm()
        return render(request, 'userview/rating_add.html', {'form': form, 'movie': movie})
    else:
        return redirect("login")
    
def rating_delete(request, rating_id):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, id=rating_id, user=request.user)
        movie = rating.movie
        rating.delete()
        messages.success(request, f'Your rating for {movie.title} has been deleted.')
        return redirect('rated')
    else:
        return redirect('login')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    
    form = NewUserForm()
    return render(request=request,template_name="userview/register.html",
                                   context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "Login successful.")
                return redirect("/")
            else:
                messages.error(request, "Unsuccessful login. User does not exist")
        messages.error(request, "Unsuccessful login. Invalid information.")
    
    form = AuthenticationForm()
    return render(request=request,template_name="userview/login.html",
                                   context={"login_form":form})


def logout_request(request):
    if not request.user.is_anonymous:
        logout(request)
        messages.success(request, "Logout successful.")
    return redirect("/")

def search(request):
    movie_title = request.GET['title'] if 'title' in request.GET else None
    genre_id = request.GET['genre'] if 'genre' in request.GET else None
    minimum_rating = request.GET['minimum_rating'] if 'minimum_rating' in request.GET else None
    genres = Genre.objects.all()
    if movie_title or genre_id or minimum_rating:
        print("searching for", movie_title, genre_id, "min rating:", minimum_rating, ".")
        movies = Movie.objects.all()
        if movie_title:
            movies = movies.filter(title__icontains=movie_title)
        if genre_id:
            movies = movies.filter(genres__id=genre_id)
        if minimum_rating:
            movies = movies.filter(average_rating__gte=minimum_rating)
            
        return render(request, 'userview/search.html', {'genres': genres, 'movies': movies})
    return render(request, 'userview/search.html', {'genres': genres})       
    
def movie_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = MovieForm()
        return render(request, 'userview/movie_add.html', {'form': form})
    else:
        return redirect("login")

def movie_edit(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movie_detail', pk=pk)
        else:
            form = MovieForm(instance=movie)
        return render(request, 'userview/movie_edit.html', {'form': form})
    else:
        return redirect("login")
    
def comment_add(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
                comment.save()
                return redirect('movie_detail', pk=movie_id)
        else:
            form = CommentForm()
        return render(request, 'userview/comment_add.html', {'form': form})
    else:
        return redirect("login")
    
def comment_delete(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=pk)
        movie = comment.movie
        if comment.user != request.user:
            messages.error(request, f'Comments from other users cannot be deleted')
        else:
            comment.delete()
            messages.success(request, f'Comment for {movie.title} has been deleted.')
        return redirect('movie_detail', pk=movie.pk)
    else:
        return redirect("login")

## admin page with a form to add a new movie
def admin_page(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Movie has been added.')
                return redirect('admin_page')
        form = MovieForm()
        return render(request, 'userview/admin_page.html', {'form': form})
    else:
        return redirect("login")

def movie_image_add(request, movie_id):
    if request.user.is_authenticated and request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_id)
        if request.method == 'POST':
            form = MovieImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.movie = movie
                image.save()
                return redirect('movie_detail', pk=movie_id)
            else:
                messages.error(request, form.errors)
                return redirect('movie_image_add', movie_id)
        
        else:
            form = MovieImageForm()
            return render(request, 'userview/movie_image_add.html', {'form': form})
    else:
        return redirect("login")
    
## home page with list of recently popular films
def home_page(request):
    movies = Movie.objects.order_by('-average_rating')[:5]
    
    template = loader.get_template('userview/home_page.html')
    context = {
        'recently_popular_movies': movies
    }
    return HttpResponse(template.render(context, request))
