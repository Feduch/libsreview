"""LibsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from schema import schema
from django.contrib.sitemaps import views
from books.sitemaps import BooksSitemap
from authors.sitemaps import AuthorsSitemap
from collection.sitemaps import CollectionSitemap
from genres.sitemaps import GenreNewSitemap
from publications.sitemaps import PublicationSitemap

sitemaps = {
    'books': BooksSitemap,
    'authors': AuthorsSitemap,
    'collection': CollectionSitemap,
    'genres': GenreNewSitemap,
    'posts': PublicationSitemap
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^', include('series.urls')),
    url(r'^', include('books.urls')),
    url(r'^', include('authors.urls')),
    url(r'^', include('publications.urls')),
    url(r'^', include('genres.urls')),
    url(r'^', include('ratings.urls')),
    url(r'^', include('search.urls')),
    url(r'^', include('info.urls')),
    url(r'^', include('navigator.urls')),
    url(r'^', include('collection.urls')),
    url(r'^', include('bot_vk.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('api_alice.urls')),
    url(r'^', include('awards.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('user_profile.urls')),
    url(r'^', include('comments.urls')),
    url(r'^', include('user.urls')),
    url(r'^', include('manager.urls')),
    url(r'^', include('subscribe.urls')),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # url(r'^api/0.1/graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^api/0.1/graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
