from django.conf.urls import url
from django.urls import path
from publications import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    url(r'^publication/$', views.PublicationList.as_view(), name='publications-list'),
    url(r'^publication/(?P<pk>\d+)/$', views.PublicationDetail.as_view(), name='publication-detail'),
    path('publication/editor/', views.publication_editor),
    path('publication/editor/get', views.vue_publication_editor_get),
    path('publication/editor/<int:pk>', views.publication_editor),
    path('publication/editor/save', views.vue_publication_save),
]
