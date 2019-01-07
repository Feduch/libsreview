from django.urls import path
from navigator import views


urlpatterns = [
    path('nav/', views.vue_navigator),
    path('nav/books/get', views.vue_get_books),
    path('nav/years/get', views.vue_get_years),
]
