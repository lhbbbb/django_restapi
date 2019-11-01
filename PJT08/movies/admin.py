from django.contrib import admin
from .models import Movie, Genre
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'audience',)

admin.site.register(Movie, MovieAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)

admin.site.register(Genre, GenreAdmin)