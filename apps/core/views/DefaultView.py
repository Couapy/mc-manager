from django.views.generic import TemplateView


class DefaultView(TemplateView):
    """This view render the default view."""

    template_name = "core/index.html"
