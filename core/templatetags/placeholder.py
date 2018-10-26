from django.template import Library
from django.templatetags.static import static

register = Library()


@register.simple_tag
def placeholder(size):
    return static('core/placeholders/placeholder{size}x{size}.png'.format(size=size))
