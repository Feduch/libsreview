from django import template

register = template.Library()


@register.inclusion_tag('publications/tags/post_inline.html')
def post_inline(posts):
    return {'posts': posts}