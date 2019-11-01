# 목표

* API 요청에 대한 이해
* RESTful API 서버 구축
* API 문서화

# 준비사항

1. (필수) Python Web Framework
   * Django 2.2.x
   * Python 3.7.x
2. (필수) Python REST Framework
   * REST API를 만들 수 있는 패키지
   * `pip install djangorestframework`
3. (선택) Django REST Swagger
   * DRF(Django REST Framework) API 문서를 자동으로 만들기 위한 패키지
   * drf-yasg
     * `pip install drf-yasg`

# 진행과정

## 1. 데이터베이스 설계

* Genre 모델 생성
* Movie 모델 생성
  * Genre 모델과 M:N(M2M) 관계로 생성
* Review 모델 생성
  * Movie 모델과 1:N 관계로 생성

## 2. Seed Data  반영

### Data Save

* `movie.json`, `genre.json` 파일을 `movies` 앱의 `fixtures/movies/` 경로로 옮김
* 명세의 데이터가 실제 모델과 매칭되지 않기 때문에 데이터 형태 변경
  * M2M 모델일 경우 .json 파일 형태에서는 [] 형태로 들어간다
  * 1:N 모델일 경우 .json 파일 형태에서 단일 숫자형태로 들어간다

### Data Load

* `python manage.py loaddata movies/genre.json`
* `python manage.py loaddata movies/movie.json`
* 위의 명령어를 통해 json 형태의 데이터들을 DB에 저장한다.

### Admin

* `python manage.py createsuperuser` 명령어로 데이터베이스에 반영되었는지 확인

## 3.  API 서버 구축

### Settings

* 프로젝트 앱의 settings.py에서 `rest_framework` Installed_APPS 변수에 추가

### URL

```python
urlpatterns = [
    path('genres/', views.genre_list, name="genre_list"),
    path('genres/<int:genre_pk>/', views.genre_detail, name="genre_detail"),
    path('movies/', views.movie_list, name="movie_list"),
    path('movies/<int:movie_pk>/', views.movie_detail, name="movie_detail"),
    path('movies/<int:movie_pk>/reviews/', views.review_list, name="review_list"),
    path('reviews/<int:review_pk>/', views.review_detail, name="review_detail"),
]
```

### Serializer

* queryset과 모델 인스턴스와 같은 복잡한 데이터를 JSON, XML 또는 다른 컨텐츠 유형으로 쉽게 변환할 수 있게 해준다
* 또한 JSON, XML 과 같은 형태로 들어오는 데이터들의 유효성 검사를 거친 후, 다시 queryset, model instance와 같은 복잡한 유형의 데이터로 파싱해줄 수도 있다
* Django의 ModelForm 클래스와 유사하게 동작

#### 1) Movie

* 패키지 설정

```python
from rest_framework import serializers
from .models import Movie, Genre, Review
```

* Serializer

```python
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'audience', 'poster_url', 'description', 'genre',)
```

```python
class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True) # models.py 에서 정의한 필드네임과 같은 이름을 써야함

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ('genre',)
```

#### 2) Genre

* Serializer

```python
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)
```

```python
class GenreDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True) # models.py 에서 M2M 필드 속성 중 related_name
    class Meta:
        model = Genre
        fields = ('id', 'movies', 'name',)
```

#### 3) Review

* Serializer

```python
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
```

### View

#### 패키지 설정

```python
from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre, Review
from .serializers import MovieSerializer, GenreSerializer, MovieDetailSerializer, GenreDetailSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
```

* Rest Framework Response
  * 렌더링되지 않은 콘텐츠를 불러와 클라이언트에게 리턴할 콘텐츠 형태로 변환
* api_view decorator
  * view가 허용된 요청을 제외하고는 405 Method Not Allowed를 응답하게 해줌

#### 1) genre list

* get 요청만 허용
* 데이터가 여러개기 때문에 many=True 옵션
* Response로 json으로 변환한 데이터 전송

```python
@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()

    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
```

#### 2) genre detail

* get 요청만 허용
* 해당 경로가 유효하지 않으면 404 not found error
* Response로 json으로 변환한 데이터 전송

```python
@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)

    serializer = GenreDetailSerializer(genre)
    return Response(serializer.data)
```

#### 3) movie list

* get 요청만 허용
* 데이터가 여러개기 때문에 many=True 옵션
* Response로 json으로 변환한 데이터 전송

```python
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()

    serializer = MovieSerializer(movies, many=True) 
    return Response(serializer.data)
```

#### 4) movie detail

- get 요청만 허용
- 해당 경로가 유효하지 않으면 404 not found error
- Response로 json으로 변환한 데이터 전송

```python
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)
```

#### 5) review create

* post 요청만 허용
* 해당 경로가 유효하지 않으면 404 not found  에러
* data=request.data 옵션으로 요청한 json 데이터를 가져와서 deserialization
* 데이터 형태가 유효한지 검사 후 유효하지 않으면 raise_exception 옵션에 의해 400 bas request 에러
* 유효하면 DB에 저장

```python
@api_view(['POST'])
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk)
    return Response({'message': '작성되었습니다.'})
```

#### 6) review update, delete

* PUT, DELETE 요청만 허용
* update는 PUT, delete는 DELETE
* 해당 경로가 유효하지 않으면 404 not found 에러
* 업데이트 때, instance 옵션을 통해서 DB에서 해당 객체를 가져옴. 이 옵션이 없으면 새로운 데이터가 DB에 추가됨
* 삭제일 시에는 serialization이 필요없음. DB에서 바로 데이터 삭제

```python
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
```

## 4. API Documents 생성

### Settings

- 프로젝트 앱의 settings.py에서 `drf_yasg` Installed_APPS 변수에 추가

### URL

* API 문서가 뜨는 페이지 경로 설정

```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
```

```python
schema_view = get_schema_view(
    openapi.Info(
        title='Movie API',
        default_version='v1',
    )
)

urlpatterns += [
    path('docs/', schema_view.with_ui('redoc'), name="api_docs"),
    path('swagger/', schema_view.with_ui('swagger'), name="api_swagger"),
]
```

## 5. 결과

* RESTful API 서버 구축
* API 자동 문서화
* PJT08 directory: 코드
* README.md
* documents directory: 스크린샷 파일들