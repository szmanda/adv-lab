from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Movie, Genre, Rating
from .forms import NewUserForm, RatingForm



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
    paginate_by = 2
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
        return context

class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre_detail.html'

class IndexView(generic.ListView):
    paginate_by = 2
    template_name = 'userview/movies_list.html'
    context_object_name = 'movies'
    def get_queryset(self):
        return Movie.objects.order_by('-title')
    
class RatedMoviesView(LoginRequiredMixin, generic.ListView):
    model = Movie
    template_name = 'userview/rated_movies_list.html'
    context_object_name = 'movies'
    paginate_by = 2

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
    minimum_rating = request.GET.get('minimum_rating')
    genres = Genre.objects.all()
    print("searching", movie_title, genre_id, minimum_rating)
    if movie_title or genre_id or minimum_rating:
        print("searching for", movie_title, genre_id, minimum_rating)
        movies = Movie.objects.all()
        if movie_title:
            movies = movies.filter(title__icontains=movie_title)
        if genre_id:
            movies = movies.filter(genres__id=genre_id)
        if minimum_rating:
            movies = movies.filter(ratings__value__gte=minimum_rating)
            
        return render(request, 'userview/search.html', {'genres': genres, 'movies': movies})
    return render(request, 'userview/search.html', {'genres': genres})       
    
def movie_add(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return redirect("login")

def movie_edit(request, pk):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return redirect("login")
    
def comment_add(request, movie_id):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return redirect("login")
    
def comment_delete(request, pk):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return redirect("login")
