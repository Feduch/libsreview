from django.urls import path
from series import views


urlpatterns = [
    path(r'book/series/', views.SeriesList.as_view(), name='series-list'),
    path(r'book/series/<int:pk>.html', views.series_detail, name='series-detail'),
]
