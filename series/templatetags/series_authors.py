from django import template
from django.db.models import Count
from books.models import Book

register = template.Library()


@register.filter(is_safe=True)
def series_authors(series):
    authors = Book.objects.filter(series=series).values('author__name', 'author').annotate(count=Count('author')).order_by('author')
    authors_list = []
    for author in authors:
        authors_list.append('<a itemprop="name" href="/a/{}/">{}</a>'.format(author['author'], author['author__name']))

    return ", ".join(authors_list)