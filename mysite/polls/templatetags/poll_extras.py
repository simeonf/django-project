from django.utils.safestring import mark_safe, esc
from django import template

register = template.Library()

@register.filter
def total_votes(poll):
    return mark_safe("<b>" + esc(poll.question) +   "</b>")

