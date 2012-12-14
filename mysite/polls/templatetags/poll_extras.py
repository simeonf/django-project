from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def total_votes(poll):
    return mark_safe(poll.question)

