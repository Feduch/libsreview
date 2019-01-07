from django.urls import path
from user import views


urlpatterns = [
    path('users/', views.users),
    path('users/<int:pk>', views.user),
    path('users/<slug:username>', views.user)
]
