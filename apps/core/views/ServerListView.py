from core.models import Server
from django.views.generic import TemplateView


class ServerListView(TemplateView):
    """This is the view for listing public servers."""

    template_name = 'core/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['servers'] = Server.objects.filter(public=True)
        return context
