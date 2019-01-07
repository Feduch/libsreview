from django import template

register = template.Library()


@register.inclusion_tag('publications/tags/book.html')
def post_book(book):
    """Возвращает книгу в виде картинки"""
    return {'book': book}