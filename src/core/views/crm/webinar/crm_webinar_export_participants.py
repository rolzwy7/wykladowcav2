import csv
from io import StringIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.models import Webinar, WebinarParticipant

CSV = "CSV"


def crm_webinar_export_participants(request, pk: int):
    """Export webinar's participants"""
    export_type = request.GET.get("export", CSV)
    webinar = get_object_or_404(Webinar, pk=pk)
    participants = (
        WebinarParticipant.manager.get_valid_participants_for_webinar((webinar))
    )
    rows = [
        [
            participant.first_name,
            participant.last_name,
            participant.email,
            participant.phone,
        ]
        for participant in participants
    ]

    # Export as CSV
    if export_type == CSV:
        buffer = StringIO()
        # buffer = BytesIO()
        csv_writer = csv.writer(buffer, delimiter=";")
        for row in rows:
            csv_writer.writerow(row)
        buffer.seek(0)
        csv_string = buffer.getvalue()
        buffer.close()
        out_filename = f"uczestnicy_szkolenie_{pk}.csv"
        response = HttpResponse(
            csv_string.encode("utf-8"),
            content_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'inline; filename="{out_filename}"'
            },
        )
        # response[
        #     "Content-Disposition"
        # ] = f'inline; filename="uczestnicy_szkolenie_{pk}.csv"'
        return response

    return HttpResponse("Invalid export type")
