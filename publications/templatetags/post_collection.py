from django import template

register = template.Library()


@register.inclusion_tag('publications/tags/collection.html')
def post_collection(collection):
    """Возвращает книгу в виде картинки"""
    return {'collection': collection}