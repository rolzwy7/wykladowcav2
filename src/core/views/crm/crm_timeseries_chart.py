"""crm_timeseries_chart"""

# flake8: noqa=E501

from django.template.response import TemplateResponse
from django.utils.timezone import now, timedelta

from core.libs.mongo.db import get_dwpldbv3_connection
from core.libs.mongo.timeseries import get_data_for_apexcharts


def crm_timeseries_chart(request):
    """crm_timeseries_chart"""

    client, db = get_dwpldbv3_connection()
    collection = db["wykladowcav2_timeseries"]

    param_charts = request.GET.get("charts")
    param_days = int(request.GET.get("days"))

    series_definitions = []
    for param_chart in param_charts.split(","):
        source, event_type = param_chart.split("-")
        print(source, event_type)
        series_definitions.append(
            {"eventType": event_type, "source": source, "data_field": "count"}
        )

    series = get_data_for_apexcharts(
        collection, series_definitions, now() - timedelta(days=param_days), now()
    )

    client.close()

    template_name = "core/pages/crm/CrmTimeseriesChart.html"
    return TemplateResponse(
        request,
        template_name,
        {"series": series["series"]},
    )
