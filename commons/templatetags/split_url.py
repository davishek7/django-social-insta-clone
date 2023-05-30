from django import template

register = template.Library()

@register.filter
def split_url(url):
    new_url = url.split('//')
    return new_url[1]