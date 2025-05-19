"""SEO Graph"""

# flake8: noqa=E501

import json

from django.template.response import TemplateResponse

from core.models import WebinarAggregate


def seo_graph_page(request):
    """seo_graph_page"""
    template_path = "core/pages/crm/seo/SeoGraphPage.html"

    aggregates = WebinarAggregate.manager.all()

    # Add aggregates
    elements = []
    parent_edges = []
    for _aggregate in aggregates:
        aggregate: WebinarAggregate = _aggregate
        grouping_token = aggregate.grouping_token
        aggregate_id = f"agg-{grouping_token}"
        elements.append(
            {
                "data": {
                    "id": aggregate_id,
                    "label": f"{aggregate_id}-{aggregate.title}",
                },
                "classes": "aggregate",
            }
        )
        # Add parent edge
        if aggregate.parent:
            parent_edges.append(
                {
                    "data": {
                        "id": f"{aggregate_id}-agg-{aggregate.parent.grouping_token}",
                        "source": aggregate_id,
                        "target": f"agg-{aggregate.parent.grouping_token}",
                    }
                }
            )

        # Add webinars
        for webinar in aggregate.webinars.all():
            webinar_id = f"web-{webinar.id}"
            link_id = f"{aggregate_id}-{webinar_id}"
            elements.append(
                {"data": {"id": webinar_id, "label": webinar_id}, "classes": "webinar"},
            )
            elements.append(
                {"data": {"id": link_id, "source": webinar_id, "target": aggregate_id}}
            )

    # Add parents edges
    for edge in parent_edges:
        elements.append(edge)

    return TemplateResponse(
        request, template_path, {"elements": json.dumps(elements, indent=4)}
    )
