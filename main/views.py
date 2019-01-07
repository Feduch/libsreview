import datetime
from itertools import zip_longest
from django.shortcuts import render, render_to_response
from publications.models import Publication
from books.models import Book
from collection.models import Collection


def index(request):
    """Главная страница """
    datetime_utc = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    datetime_utc_book = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    books = Book.objects.filter(date_create__gte=datetime_utc_book)[:20]
    publications = Publication.objects.filter(date_create__gte=datetime_utc).order_by('-rating', '-show_counter')
    collections = Collection.objects.filter(date_create__gte=datetime_utc).order_by('-rating', '-show_counter')

    best_list = []
    #
    for item in zip_longest(books, publications, collections, fillvalue=None):
        best_list += (list(item))

    books = Book.objects.filter().order_by('-date_create')[:20]
    publications = Publication.objects.filter().order_by('-date_create')[:20]
    collections = Collection.objects.filter().order_by('-date_create')[:20]

    all_list = []
    for item in zip_longest(books, publications, collections, fillvalue=None):
        all_list += (list(item))

    to_template = {
        "all": [e for e in all_list if e],
        "best": [e for e in best_list if e]
    }

    return render(request, 'index.html', to_template)


def robots(request):
    return render_to_response('robots.txt', content_type="text/plain")


def handler404(request, exception=None, template_name='404.html'):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
