from io import BytesIO
from pathlib import Path

from borb.pdf import (
    PDF,
    Document,
    Page,
    PageLayout,
    Paragraph,
    SingleColumnLayout,
)
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from django.conf import settings
from django.template.defaultfilters import date as _date

from core.models import WebinarCertificate


class CertificateFonts:
    """Certificate fonts"""

    CambriaBold = "CambriaBold.ttf"
    CambriaBolder = "CambriaBolder.TTF"
    CambriaItalic = "CambriaItalic.ttf"
    CambriaRegular = "CambriaRegular.ttf"
    LatoBold = "LatoBold.ttf"
    LatoRegular = "LatoRegular.ttf"


def load_font(font_name: str):
    """Load font from assets"""
    font_path: Path = (
        settings.BASE_DIR.parent / "core" / "assets" / "fonts" / font_name
    )
    return TrueTypeFont.true_type_font_from_file(font_path.absolute())


class CertificateService:
    """Certificate service"""

    def __init__(self, certificate: WebinarCertificate) -> None:
        self.certificate = certificate
        self.pdf = self.create_pdf()

    def create_pdf(self) -> Document:
        # template_path: Path = (
        #     settings.BASE_DIR.parent
        #     / "core"
        #     / "assets"
        #     / "certificate"
        #     / "certificate.pdf"
        # )

        # with template_path.open("rb") as src:
        #     buffer = BytesIO(src.read())
        #     doc = PDF.loads(buffer)

        # # create Document
        doc: Document = Document()

        # create Page
        # page: Page = doc.get_page(0)
        page: Page = Page()

        # page: Page = Page()
        doc.add_page(page)

        # PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        cambria_regular = load_font(CertificateFonts.CambriaRegular)

        # add Paragraph
        layout.add(Paragraph(self.certificate.first_name, font=cambria_regular))
        layout.add(Paragraph(self.certificate.last_name, font=cambria_regular))
        layout.add(
            Paragraph(
                self.certificate.title,
                font=cambria_regular,
            )
        )
        layout.add(Paragraph(self.certificate.hours, font=cambria_regular))
        layout.add(
            Paragraph(
                _date(self.certificate.issue_date, "j E Y"),
                font=cambria_regular,
            )
        )

        # return
        return doc

    def get_pdf_bytes(self) -> bytes:
        """This function converts a borb.pdf.Document to bytes"""
        buffer = BytesIO()
        PDF.dumps(buffer, self.pdf)
        buffer.seek(0)
        return buffer.getvalue()
