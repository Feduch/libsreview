from django.urls import path
from subscribe import views

urlpatterns = [
    path('api/subscribe', views.subscribe),
]
