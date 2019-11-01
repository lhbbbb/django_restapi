from rest_framework import serializers
from .models import Movie, Genre, Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'audience', 'poster_url', 'description', 'genre',)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)

class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ('genre',)

class GenreDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = Genre
        fields = ('id', 'movies', 'name',)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'