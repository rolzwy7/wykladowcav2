from django.views.generic import DetailView, ListView

from core.models import CrmContact


class CrmContactDetail(DetailView):
    """CRM company detail"""

    template_name = "core/pages/crm/contact/CrmContactDetail.html"
    queryset = CrmContact.objects.all()


class CrmContactList(ListView):
    """CRM compant list"""

    template_name = "core/pages/crm/contact/CrmContactList.html"
    queryset = CrmContact.objects.all()
