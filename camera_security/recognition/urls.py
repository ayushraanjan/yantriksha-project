from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('video-feed', views.video_feed, name='video'),
]
