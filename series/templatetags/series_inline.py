from django import template

register = template.Library()


@register.inclusion_tag('series/tags/series_inline.html')
def series_inline(series):
    """Возвращает серию"""
    return {'series': series}