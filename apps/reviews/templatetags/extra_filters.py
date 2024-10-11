from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Retourne une plage (range) de 0 à la valeur donnée."""
    return range(value)
