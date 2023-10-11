from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


# Create your views here.
def staff_or_admin(user):
    return user.is_staff or user.is_superuser


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_or_admin), name='dispatch')
class AdminPanelComponentsView(TemplateView):
    template_name = 'adminpanel/components.html'
