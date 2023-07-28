# flake8: noqa:submitter.email
# pylint: disable=line-too-long
import io
from decimal import Decimal
from pathlib import Path

from borb.pdf import (
    PDF,
    Alignment,
    Document,
    FlexibleColumnWidthTable,
    HexColor,
    Image,
    Page,
    PageLayout,
    Paragraph,
    SingleColumnLayout,
    TableCell,
)
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.layout_element import LayoutElement
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.urls import reverse

from core.consts.exemptions_consts import PRICE_ADNOTATION
from core.models import (
    WebinarApplication,
    WebinarApplicationCompany,
    WebinarApplicationInvoice,
    WebinarApplicationSubmitter,
)

COMPANY_NAME = settings.COMPANY_NAME
COMPANY_NAME_FULL = settings.COMPANY_NAME_FULL
COMPANY_OFFICE_EMAIL = settings.COMPANY_OFFICE_EMAIL
BASE_DIR = settings.BASE_DIR
BASE_URL = settings.BASE_URL
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"
LOGO_PATH: Path = ASSETS_DIR / "pdf_card" / "logo_pdf_card.png"


class PdfCardFonts:
    """Certificate fonts"""

    LatoRegular = "LatoRegular.ttf"
    LatoBold = "LatoBold.ttf"


def load_font(font_name: str):
    """Load font from assets directory"""
    font_path = ASSETS_DIR / "fonts" / font_name
    return TrueTypeFont.true_type_font_from_file(font_path)


class ApplicationPdfCardService:
    """Service for generating PDF application card"""

    def __init__(self, application: WebinarApplication) -> None:
        self.application = application
        self.pdf: Document = Document()
        self.page: Page = Page()
        self.pdf.add_page(self.page)
        self.layout: PageLayout = SingleColumnLayout(
            self.page,
            vertical_margin=Decimal(10),
            horizontal_margin=Decimal(10),
        )

        self.number_of_columns = 12
        self.number_of_rows = 14

        self.number_of_rows += self.application.participants.count()

        if self.application.recipient:
            self.number_of_rows += 3

        self.table = FlexibleColumnWidthTable(
            number_of_columns=self.number_of_columns,
            number_of_rows=self.number_of_rows,
        )

        self.font_regular = load_font(PdfCardFonts.LatoRegular)
        self.font_bold = load_font(PdfCardFonts.LatoBold)

    def _add_submitter_row(self, submitter):
        self._add_header_row("Osoba zgłaszająca")
        self.table.add(
            TableCell(
                Paragraph(
                    "Imię:",
                    font=self.font_bold,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    submitter.first_name,
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Nazwisko:",
                    font=self.font_bold,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    submitter.last_name,
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "E-mail:",
                    font=self.font_bold,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    submitter.email,
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Numer telefonu:",
                    font=self.font_bold,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    submitter.phone,
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )

    def _add_header_row(self, header_title):
        """Add header row"""
        self.table.add(
            TableCell(
                Paragraph(
                    header_title.upper(),
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=self.number_of_columns,
                background_color=HexColor("D3D3D3"),
            )
        )

    def _add_table_cell(
        self,
        layout_element: LayoutElement,
        column_span: int,
        background_color: HexColor,
    ):
        """Add table cell"""
        self.table.add(
            TableCell(
                layout_element,
                column_span=column_span,
                background_color=background_color,
                padding_top=Decimal(15),
            )
        )

    def _add_company(self, company: WebinarApplicationCompany):
        """Add company"""

        self._add_table_cell(
            Paragraph(
                "Nazwa:",
                font=self.font_bold,
            ),
            column_span=3,
            background_color=HexColor("D3D3D3"),
        )

        self.table.add(
            TableCell(
                Paragraph(
                    company.name,
                    font=self.font_regular,
                ),
                column_span=9,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "NIP:",
                    font=self.font_bold,
                ),
                column_span=1,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    company.nip,
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Adres:",
                    font=self.font_bold,
                ),
                column_span=2,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    company.address,
                    font=self.font_regular,
                ),
                column_span=6,
            )
        )

    def _add_participants_row(self):
        self._add_header_row("Uczestnicy szkolenia")
        self.table.add(
            TableCell(
                Paragraph(
                    "Imię",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Nazwisko",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Adres e-mail",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Numer telefonu",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )

        for participant in self.application.participants:
            self.table.add(
                TableCell(
                    Paragraph(
                        participant.first_name,
                        font=self.font_regular,
                    ),
                    column_span=3,
                )
            )
            self.table.add(
                TableCell(
                    Paragraph(
                        participant.last_name,
                        font=self.font_regular,
                    ),
                    column_span=3,
                )
            )
            self.table.add(
                TableCell(
                    Paragraph(
                        participant.email,
                        font=self.font_regular,
                    ),
                    column_span=3,
                )
            )
            self.table.add(
                TableCell(
                    Paragraph(
                        participant.phone,
                        font=self.font_regular,
                    ),
                    column_span=3,
                )
            )

    def create_pdf(self):
        """Create PDF application card"""

        self.layout.add(
            Image(
                LOGO_PATH,
                width=Decimal(150),
                height=Decimal(25),
            )
        )

        self.layout.add(
            Paragraph(
                f"Karta Zgłoszeniowa - {COMPANY_NAME}\n"
                "Prosimy o odesłanie podpisanej karty"
                f" na adres e-mail: {COMPANY_OFFICE_EMAIL}",
                font=self.font_bold,
                horizontal_alignment=Alignment.CENTERED,
                text_alignment=Alignment.CENTERED,
                respect_newlines_in_text=True,
            )
        )

        self.layout.add(
            Paragraph(
                f"Zgłoszenie numer: {self.application.uuid}",
                font=self.font_regular,
                horizontal_alignment=Alignment.CENTERED,
                text_alignment=Alignment.CENTERED,
                respect_newlines_in_text=True,
            )
        )

        self._add_header_row("Dane szkolenia")

        self.table.add(
            TableCell(
                Paragraph("Szkolenie:", font=self.font_bold),
                column_span=4,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    self.application.webinar.title,
                    font=self.font_regular,
                ),
                column_span=8,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Termin szkolenia:",
                    font=self.font_bold,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    _date(self.application.webinar.date, "j E Y H:i"),
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    "Cena NETTO (za uczestnika):",
                    font=self.font_bold,
                ),
                column_span=3,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    f"{self.application.total_price_netto} zł {PRICE_ADNOTATION}",
                    font=self.font_regular,
                ),
                column_span=3,
            )
        )

        self._add_participants_row()

        buyer = self.application.buyer
        if buyer:
            self._add_header_row("Nabywca")
            self._add_company(buyer)

        recipient = self.application.recipient
        if recipient:
            self._add_header_row("Odbiorca")
            self._add_company(recipient)

        submitter: WebinarApplicationSubmitter = self.application.submitter  # type: ignore
        if submitter:
            self._add_submitter_row(submitter)

        invoice: WebinarApplicationInvoice = self.application.invoice  # type: ignore
        vat_exemption_display = invoice.get_vat_exemption_display()  # type: ignore

        self.table.add(
            TableCell(
                Paragraph(
                    "E-mail (faktura):",
                    font=self.font_bold,
                ),
                column_span=4,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    invoice.invoice_email,
                    font=self.font_regular,
                ),
                column_span=8,
            )
        )

        self.table.add(
            TableCell(
                Paragraph(
                    "Zwolnienie z VAT:",
                    font=self.font_bold,
                ),
                column_span=4,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    vat_exemption_display,
                    font=self.font_regular,
                ),
                column_span=8,
            )
        )

        self.table.add(
            TableCell(
                Paragraph(
                    "Dodatkowe uwagi:",
                    font=self.font_bold,
                ),
                column_span=4,
                background_color=HexColor("D3D3D3"),
            )
        )
        self.table.add(
            TableCell(
                Paragraph(
                    self.application.additional_information or "Brak",
                    font=self.font_regular,
                ),
                column_span=8,
            )
        )

        self.layout.add(self.table)

        self.layout.add(
            Paragraph(
                " ".join(
                    [
                        "Przesłanie karty zgłoszenia stanowi potwierdzenie",
                        "przyjęcia oferty oraz potwierdzenie zapoznania się z",
                        "regulaminem świadczenia usług szkoleniowych",
                        "dostępnym na stronie",
                        f"{BASE_URL}{reverse('core:terms_and_conditions_webinars')}",
                    ]
                ),
                font=self.font_regular,
                horizontal_alignment=Alignment.LEFT,
                text_alignment=Alignment.LEFT,
                respect_newlines_in_text=True,
            )
        )

        table_signatures = FlexibleColumnWidthTable(
            number_of_columns=12,
            number_of_rows=2,
            border_top=False,
            border_right=False,
            border_bottom=False,
            border_left=False,
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "\n\n\n",
                    font=self.font_bold,
                    respect_newlines_in_text=True,
                ),
                column_span=4,
            )
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "\n\n\n",
                    font=self.font_bold,
                    respect_newlines_in_text=True,
                ),
                column_span=4,
            )
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "\n\n\n",
                    font=self.font_bold,
                    respect_newlines_in_text=True,
                ),
                column_span=4,
            )
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "Pieczątka firmowa",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=4,
            )
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "Miejscowość, data",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=4,
            )
        )

        table_signatures.add(
            TableCell(
                Paragraph(
                    "Podpis osoby upoważnionej",
                    font=self.font_bold,
                    horizontal_alignment=Alignment.CENTERED,
                    text_alignment=Alignment.CENTERED,
                ),
                column_span=4,
            )
        )

        self.layout.add(table_signatures)

        return self

    def to_bytes(self) -> bytes:
        """Get PDF bytes"""
        buffer = io.BytesIO()
        PDF.dumps(buffer, self.pdf)
        buffer.seek(0)
        return buffer.getvalue()
