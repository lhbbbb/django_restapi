from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.CharField(max_length=150)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.content