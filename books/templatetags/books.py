from django import template

register = template.Library()


@register.inclusion_tag('books/tags/books.html')
def books(books):
    """Возвращает книгу в виде картинки"""
    return {'books': books}