from django.urls import path
from . import views

urlpatterns = [
  path("<int:id>/", views.cat.get),
  path("<int:id>/comment/", views.comment.get),
  path("<int:id>/comment/create/", views.comment.create),
  path("<int:id>/image/create/", views.cat.create_image),
  path("list/", views.cat.getlist),
  path("create/", views.cat.create),
]