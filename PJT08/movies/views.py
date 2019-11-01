from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre, Review
from .serializers import MovieSerializer, GenreSerializer, MovieDetailSerializer, GenreDetailSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()

    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)

    serializer = GenreDetailSerializer(genre)
    return Response(serializer.data)

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()

    serializer = MovieSerializer(movies, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk)
    return Response({'message': '작성되었습니다.'})

@api_view(['PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "PUT":
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message': '수정되었습니다.'})
    else:
        review.delete()
        return Response({'message': '삭제되었습니다.'})
