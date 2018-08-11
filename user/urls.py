from django.urls import path
from . import views

urlpatterns = [
  path("twitter_login/", views.twitter_login),
  path("google_login/", views.google_login),
]