from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import EmbeddedVideoItem

class IndexView(generic.ListView):
    paginate_by = 10
    template_name = 'embed/index.html'
    context_object_name = 'videos'
    def get_queryset(self):
        return EmbeddedVideoItem.objects.order_by('title')

def index(request: HttpRequest):
    videos = EmbeddedVideoItem.objects.order_by('title')
    template = loader.get_template('embed/index.html')
    context = {
        'videos': videos
    }
    return HttpResponse(template.render(context, request))

def player(request: HttpRequest, video_id: int):
    video = get_object_or_404(EmbeddedVideoItem, pk=video_id)
    template = loader.get_template('embed/player.html')
    context = {
        'video_object': video
    }
    print(video.video)
    return HttpResponse(template.render(context, request))

def example(request):
    videos = EmbeddedVideoItem.objects.all()
    return render(request, 'embed/example.html', context={'videos': videos})