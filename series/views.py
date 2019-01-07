from django.conf import settings
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView
from series.models import Series
from books.models import Book
from publications.models import Publication


class SeriesList(ListView):
    """
    Список серий
    """
    model = Series
    context_object_name = 'series'
    paginate_by = settings.PAGE_SIZE
    queryset = Series.objects.all().order_by('-image', '-show_counter')


def series_detail(request, pk=None):
    series = Series.objects.get(pk=pk)

    series.show_counter += 1
    series.save(update_fields=['show_counter'])

    # посты
    posts = Publication.objects.filter(series=pk)
    books = Book.objects.prefetch_related('author', 'genre_new').filter(series=pk).order_by('year')

    authors = list(books.values('author__id','author__name').annotate(count=Count('author__id')).order_by('author__id'))
    genres = list(books.values('genre__title', 'genre__slug').annotate(count=Count('genre__slug')).order_by('genre__slug'))

    to_template = {
        'series': series,
        'posts': posts,
        'book_series': books,
        'authors': authors,
        'genres': genres
    }

    return render(request, 'series/series_detail.html', to_template)