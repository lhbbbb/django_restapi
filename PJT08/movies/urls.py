from django.urls import path
from . import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Movie API',
        default_version='v1',
    )
)

app_name = "movies"

urlpatterns = [
    path('genres/', views.genre_list, name="genre_list"),
    path('genres/<int:genre_pk>/', views.genre_detail, name="genre_detail"),
    path('movies/', views.movie_list, name="movie_list"),
    path('movies/<int:movie_pk>/', views.movie_detail, name="movie_detail"),
    path('movies/<int:movie_pk>/reviews/', views.review_list, name="review_list"),
    path('reviews/<int:review_pk>/', views.review_detail, name="review_detail"),
    path('docs/', schema_view.with_ui('redoc'), name="api_docs"),
    path('swagger/', schema_view.with_ui('swagger'), name="api_swagger"),
]