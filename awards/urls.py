from django.urls import path
from awards import views


urlpatterns = [
    path('awards/get', views.vue_awards_get)
]
