from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Rating, Movie, Genre

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
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    imdb_reference = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Movie
        fields = ('title', 'genres', 'imdb_reference')
    