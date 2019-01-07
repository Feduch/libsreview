from django import template

register = template.Library()


@register.inclusion_tag('books/tags/book_cover.html')
def book_cover(book):
    """Возвращает книгу в виде картинки"""
    return {'book': book}