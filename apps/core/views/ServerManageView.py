from core.models import Server, ServerShare
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class ServerManageView(TemplateView):
    """This view render the user server list."""

    template_name = 'core/manage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['servers'] = Server.objects.filter(owner=self.request.user)
        shares = ServerShare.objects.filter(user=self.request.user)
        context['shared_servers'] = [ share.server for share in shares ]
        return context
