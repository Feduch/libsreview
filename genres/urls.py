from django.urls import path
from genres import views


urlpatterns = [
    path('genre/', views.genres_list, name='genre-list'),
    path('genre/<slug:slug>/', views.GenreDetail.as_view(), name='genre-detail'),
    path('genres/get', views.vue_genres_get)
]
