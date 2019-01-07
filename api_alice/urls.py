from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from api_alice import views

urlpatterns = [
    url(r'^api_alice/$', views.index, name='alice_index'),
    url(r'^api_alice_buy/$', views.alice_buy, name='alice_buy'),
]