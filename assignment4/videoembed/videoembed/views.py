from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import EmbeddedVideoItem
def index(request):
    videos = EmbeddedVideoItem.objects.all()
    return render(request, 'index.html', context={'videos': videos})
