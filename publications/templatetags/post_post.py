from django import template

register = template.Library()


@register.inclusion_tag('publications/tags/post.html')
def post_post(post):
    """Возвращает книгу в виде картинки"""
    return {'post': post}