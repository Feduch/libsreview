from django.conf.urls import url
from django.urls import path
from authors import views


urlpatterns = [
    path('a/', views.author_list, name='authors-list'),
    url(r'^a/(?P<pk>\d+)/$', views.AuthorDetail.as_view(), name='author-detail'),
    path('author/genres/get', views.get_author_book_genres),
    path('author/books/get', views.get_author_books),
    path('authors/get', views.vue_get_authors),
]
