from django.template import Library


register = Library()


@register.simple_tag(takes_context=True)
def is_authorized(context, *controls):
    """Return true is the current user is allowed to acccess to server context variable."""
    server = context['server']
    user = context['user']
    return server.is_authorized(user, controls)
