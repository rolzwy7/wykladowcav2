"""
Service for webinar certificate generation
"""

# flake8: noqa=E501
# pylint: disable=line-too-long

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.template.defaultfilters import date as _date
from PIL import Image, ImageDraw

from core.models import WebinarCertificate
from core.utils.pillow import (
    draw_centered_text,
    draw_multiline_centered_text,
    load_font,
)

COMPANY_NAME_FULL = settings.COMPANY_NAME_FULL
BASE_DIR = settings.BASE_DIR
ASSETS_DIR: Path = BASE_DIR.parent / "core" / "assets"
RGBA = "RGBA"


class CertificateFonts:
    """Certificate fonts"""

    AleoBlack = "AleoBlack.ttf"
    AleoBlackItalic = "AleoBlackItalic.ttf"
    AleoBold = "AleoBold.ttf"
    AleoBoldItalic = "AleoBoldItalic.ttf"
    AleoExtraBold = "AleoExtraBold.ttf"
    AleoExtraBoldItalic = "AleoExtraBoldItalic.ttf"
    AleoExtraLight = "AleoExtraLight.ttf"
    AleoExtraLightItalic = "AleoExtraLightItalic.ttf"
    AleoItalic = "AleoItalic.ttf"
    AleoLight = "AleoLight.ttf"
    AleoLightItalic = "AleoLightItalic.ttf"
    AleoMedium = "AleoMedium.ttf"
    AleoMediumItalic = "AleoMediumItalic.ttf"
    AleoRegular = "AleoRegular.ttf"
    AleoSemiBold = "AleoSemiBold.ttf"
    AleoSemiBoldItalic = "AleoSemiBoldItalic.ttf"
    AleoThin = "AleoThin.ttf"
    AleoThinItalic = "AleoThinItalic.ttf"
    CambriaBold = "CambriaBold.ttf"
    CambriaBolder = "CambriaBolder.ttf"
    CambriaItalic = "CambriaItalic.ttf"
    CambriaRegular = "CambriaRegular.ttf"
    LatoBold = "LatoBold.ttf"
    LatoRegular = "LatoRegular.ttf"


class CertificateService:
    """Certificate service"""

    def __init__(self, certificate: WebinarCertificate) -> None:
        self.certificate = certificate

    def get_pdf_bytes(self) -> bytes:
        """Create PDF"""

        # Path to certificate template
        template_path: Path = ASSETS_DIR / "certificate" / "certificate.png"

        # Open template certificate in image format with PIL
        template_layer = Image.open(template_path).convert("RGB")

        # Create transparent layer
        transparent_layer = Image.new(
            RGBA,
            (template_layer.width, template_layer.height),
            (255, 0, 0, 0),
        )

        # Draw on transparent layer
        draw = ImageDraw.Draw(transparent_layer)

        # Draw organizer stamp
        stamp_path: Path = ASSETS_DIR / "certificate" / "stamp.png"
        stamp_im = Image.open(stamp_path).convert("RGBA")
        stamp_factor = 2.5
        logo_im = stamp_im.resize(
            (
                int(stamp_im.width / stamp_factor),
                int(stamp_im.height / stamp_factor),
            )
        )
        transparent_layer.paste(
            logo_im,
            (550, 3_020),
        )

        # Draw organizer signature
        signature_path: Path = ASSETS_DIR / "certificate" / "signature.png"
        signature_im = Image.open(signature_path).convert("RGBA")
        signature_factor = 2.5
        logo_im = signature_im.resize(
            (
                int(signature_im.width / signature_factor),
                int(signature_im.height / signature_factor),
            )
        )
        transparent_layer.paste(
            logo_im,
            (2130, 3130),
        )

        # Draw "Mr/Mrs" title
        font = load_font(CertificateFonts.AleoLight, 70)
        draw_centered_text(draw, template_layer, font, "Pan/i", x=0, y=-750)

        # Draw "Participated in ..." text
        font = load_font(CertificateFonts.AleoLight, 70)
        temp_text = "Uczestniczył/a w szkoleniu pod tytułem:"
        draw_centered_text(draw, template_layer, font, temp_text, x=0, y=-300)

        # Draw "Organized by ..." text
        font = load_font(CertificateFonts.AleoLight, 70)
        temp_text = "Zorganizowanym przez:"
        draw_centered_text(draw, template_layer, font, temp_text, x=0, y=350)

        # Draw participant fullname

        fullname = f"{self.certificate.first_name} {self.certificate.last_name}"
        fullname_fs = 200 if len(fullname) < 20 else 150
        font = load_font(CertificateFonts.AleoLight, fullname_fs)
        draw_multiline_centered_text(
            draw,
            template_layer,
            font,
            fullname,
            x=0,
            x_delta=0,
            y=-600,
            y_delta=fullname_fs,
            max_width_px=2600,
        )

        # Draw webinar title
        webinar_title = self.certificate.title
        webinar_title_fs = 90 if len(webinar_title) < 200 else 75
        font = load_font(CertificateFonts.AleoLightItalic, webinar_title_fs)

        draw_multiline_centered_text(
            draw,
            template_layer,
            font,
            webinar_title,
            x=0,
            x_delta=0,
            y=-150,
            y_delta=100,
            max_width_px=2000,
        )

        # Draw organizer name
        font = load_font(CertificateFonts.AleoBold, 50)
        draw_centered_text(draw, template_layer, font, COMPANY_NAME_FULL, x=0, y=450)

        # Draw webinar date adnotation
        font = load_font(CertificateFonts.AleoBold, 50)
        webinar_date = f"dnia {_date(self.certificate.issue_date, 'j E Y')}r."
        draw_centered_text(draw, template_layer, font, webinar_date, x=0, y=510)

        # Draw webinar duration adnotation
        font = load_font(CertificateFonts.AleoBold, 50)
        webinar_duration = f"zajęcia obejmowały {self.certificate.hours} wykładów"
        draw_centered_text(draw, template_layer, font, webinar_duration, x=0, y=570)

        # Draw certificate number adnotation
        font = load_font(CertificateFonts.AleoBold, 50)
        issue_date = _date(self.certificate.issue_date, "Y/m")
        certificate_id: int = self.certificate.id + 365  # type: ignore
        certificate_number = f"Certyfikat Nr {issue_date}/{certificate_id}"
        draw_centered_text(draw, template_layer, font, certificate_number, x=0, y=630)

        # Paste transparent layer over template layer
        template_layer.paste(transparent_layer, (0, 0), transparent_layer)

        # Create byte buffer
        pdf_bytes = BytesIO()

        # Save PDF bytes to buffer
        template_layer.save(pdf_bytes, format="PDF", save_all=True)

        # Get and return PDF bytes
        return pdf_bytes.getvalue()
