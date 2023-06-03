from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Rating, Movie, Genre, Comment, MovieImage

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user
    
class RatingForm(forms.ModelForm):
    value = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Rating
        fields = ('value',)

class MovieForm(forms.ModelForm):
    front_image = forms.ModelChoiceField(
        queryset=MovieImage.objects.all(),
        required=False,
        empty_label='No front image'
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'genres', 'imdb_reference', 'front_image']

class MovieImageForm(forms.ModelForm):
    image = forms.ImageField(max_length=100000000)
    class Meta:
        model = MovieImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
