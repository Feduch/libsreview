from django.urls import path
from info import views


urlpatterns = [
    path('info/right/', views.right),
    path('info/rule/', views.rule)
]
