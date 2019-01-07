from django import template

register = template.Library()


@register.inclusion_tag('books/tags/books_inline.html')
def books_inline(books):
    """Возвращает книгу в виде картинки"""
    return {'books': books}
