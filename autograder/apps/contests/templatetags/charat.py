from django import template

register = template.Library()


@register.filter
def char_at(value, index):
    try:
        return value[int(index)]
    except (IndexError, ValueError, TypeError):
        return ""
