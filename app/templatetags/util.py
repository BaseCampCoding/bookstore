from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    querydict = context.request.GET.copy()
    for key, value in kwargs.items():
        querydict[key] = value
    return querydict.urlencode()
