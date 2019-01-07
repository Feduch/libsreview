from django.conf.urls import url
from django.urls import path
from books import views


urlpatterns = [
    url(r'^book/$', views.book_list, name='books-list'),
    url(r'^book/(?P<pk>\d+)/$', views.book_detail, name='book-detail'),
    path('book/<int:pk>/read', views.read, name='book-read'),
    path('book/genre/place/', views.genre_place),
    path('book/year/place/', views.year_place),
    path('book/genre/year/place/', views.genre_year_place),
    path('books/get', views.vue_get_books),
    path('book/litres/set', views.vue_set_litres_id),
    path('book/import/', views.import_books),
    path('book/import/get', views.vue_get_import_books),
    path('book/import/status/set', views.vue_set_import_books_status),
    path('book/editor/', views.editor),
    path('book/editor/get', views.vue_book_editor_get),
    path('book/editor/<int:pk>', views.editor),
    path('book/editor/save', views.vue_book_save),
    path('book/editor/authors/get', views.vue_book_editor_authors_get),
    path('book/editor/series/get', views.vue_book_editor_series_get),
    path('book/editor/books/get', views.vue_collection_editor_books_get),
    path('book/manager/partner/link/count', views.vue_book_partner_link),
    url(r'^test/book/(?P<pk>\d+)/$', views.test_book_detail, name='test-book-detail'),
]
