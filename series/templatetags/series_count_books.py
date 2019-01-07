from django import template
from books.models import Book

register = template.Library()


@register.filter(is_safe=True)
def series_count_books(series):
    return Book.objects.filter(series=series).count()