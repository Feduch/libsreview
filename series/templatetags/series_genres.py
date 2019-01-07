from django import template
from django.db.models import Count
from books.models import Book

register = template.Library()


@register.filter(is_safe=True)
def series_genres(series):
    genres = Book.objects.filter(series=series).values('genre__title', 'genre__slug').annotate(
        count=Count('genre__slug')).order_by('genre__slug')

    genre_list = []
    for genre in genres:
        genre_list.append('<a itemprop="name" href="/genre/{}/">{}</a>'.format(genre['genre__slug'], genre['genre__title']))

    return ", ".join(genre_list)