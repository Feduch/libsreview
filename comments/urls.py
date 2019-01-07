from django.urls import path
from comments import views


urlpatterns = [
    path('comments/get', views.get),
    path('comments/set', views.set)
]
