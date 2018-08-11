from django.contrib import admin
from .models import Cat, Area, CatImage, CatComment

admin.site.register([Cat, Area, CatImage, CatComment])