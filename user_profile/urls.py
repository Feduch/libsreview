from django.urls import path
from user_profile import views


urlpatterns = [
    path('accounts/profile', views.index),
    path('accounts/profile/get', views.get),
    path('accounts/profile/save', views.save),
    path('accounts/profile/login', views.singin),
    path('accounts/profile/reg', views.reg),
    path('accounts/profile/reset', views.reset),
    path('accounts/profile/avatar/save', views.avatar_save),
]
