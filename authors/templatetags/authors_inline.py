from django import template

register = template.Library()


@register.inclusion_tag('authors/tags/authors_inline.html')
def authors_inline(authors):
    """Возвращает книгу в виде картинки"""
    return {'authors': authors}