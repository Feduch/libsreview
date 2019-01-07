from django.conf.urls import url
from django.urls import path
from ratings import views

urlpatterns = [
    path('best-100/', views.best_100, name='rating-best-100'),
    path('best-today/', views.best_for_today, name='rating-best-today'),
    path('best-week/', views.best_for_week, name='rating-best-week'),
    path('best-100-russian/', views.best_russian, name='rating-best-russian'),
    path('best-interesting/', views.best_libs, name='rating-best-libs'),
    path('best-online/', views.best_online, name='rating-best-online'),
    path('best-month/', views.best_for_month, name='rating-best-month'),
    url(r'^ratings/best-sellers/$', views.best_sellers, name='rating-best-sellers'),
    url(r'^ratings/best-world/$', views.best_world, name='rating-best-world'),
    path('best-<int:year>/', views.best_year, name='rating-best-year'),
    path('best-<int:year>-<slug:month>/', views.best_month_year, name='rating-best-month-year'),
    url(r'^ratings/best-genres/$', views.best_genres, name='rating-best-genres'),
    url(r'^ratings/best-popadanci/$', views.best_popadanci, name='rating-best-popadanci'),
    url(r'^ratings/best-magic/$', views.best_magic, name='rating-best-magic'),
    url(r'^ratings/$', views.all),
    url(r'^clear-cache/$', views.clear_all_cache),
    path('ratings/author/set', views.author_set),
    path('ratings/book/set', views.book_set),
    path('ratings/publication/set', views.publication_set),
    path('ratings/collection/set', views.collection_set),
]