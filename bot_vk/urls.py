from django.urls import path
from bot_vk import views

urlpatterns = [
    path('bot_debug_vk/', views.bot_debug_vk),
    path('bot_vk_best_fantasy/', views.bot_vk_best_fantasy),
    path('subscr_vk_fantasy/', views.bot_vk_fantasy_subscr),
    path('post_wall_vk_fantasy/', views.bot_vk_post_to_wall),
]