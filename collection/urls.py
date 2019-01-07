from django.urls import path
from collection import views


urlpatterns = [
    path('collections/', views.CollectionsList.as_view(), name='collection-list'),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
    path('collections/books/get', views.vue_get_collection_books),
    path('collections/editor/', views.collection_editor),
    path('collections/editor/get', views.vue_collection_editor_get),
    path('collections/editor/<int:pk>', views.collection_editor),
    path('collections/editor/save', views.vue_collection_save)
]
