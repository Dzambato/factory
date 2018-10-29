from django.template import Library

register = Library()


LABEL_DANGER = 'danger'
LABEL_SUCCESS = 'success'
LABEL_DEFAULT = 'default'

@register.inclusion_tag('dashboard/includes/_page_availability.html')
def render_page_availability(page):
    ctx = {'is_published': page.is_published, 'page': page}
    if page.is_published:
        label_cls = LABEL_SUCCESS
        ctx.update({'label_cls': label_cls})
    return ctx

