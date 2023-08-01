from django.views.generic import DetailView, ListView

from core.models import CrmCompany


class CrmCompanyDetail(DetailView):
    """CRM company detail"""

    template_name = "core/pages/crm/company/CrmCompanyDetail.html"
    queryset = CrmCompany.objects.all()


class CrmCompanyList(ListView):
    """CRM compant list"""

    template_name = "core/pages/crm/company/CrmCompanyList.html"
    queryset = CrmCompany.objects.all()
