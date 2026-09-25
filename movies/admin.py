from django.contrib import admin
from .models import Genre, Movie, TheaterLink

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(TheaterLink)
