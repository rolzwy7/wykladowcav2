# flake8: noqa:F841
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
# pylint: disable=no-name-in-module

from typing import Optional

from django.conf import settings
from lxml import etree
from pydantic import BaseModel
from requests import Session
from zeep import Client
from zeep.transports import Transport

from core.libs.validators.nip_validator import validate_nip


class RegonCompany(BaseModel):
    """Represents company result from REGON Api"""

    nip: str
    name: str
    address: str
    postal_code: str
    city: str


class RegonAutocompleteResponse(BaseModel):
    """Represents autocomplete response"""

    success: bool
    error: Optional[str]
    company: Optional[RegonCompany]


class RegonService:
    """Service for REGON"""

    base_url = "https://wyszukiwarkaregon.stat.gov.pl"
    wsdl_path = "/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl"
    service_path = "/wsBIR/UslugaBIRzewnPubl.svc"
    namespace = "{http://tempuri.org/}e3"

    def __init__(self) -> None:
        self.wsdl = f"{self.base_url}{self.wsdl_path}"
        self.service_url = f"{self.base_url}{self.service_path}"

    def _create_service(self, client: Client):
        """Create REGON client"""
        return client.create_service(
            self.namespace,
            self.service_url,
        )

    def create_authenticated_service(self):
        """Create authenticated REGON service"""

        # Prepare client and service
        client = Client(wsdl=self.wsdl)
        service = self._create_service(client)

        # Log in
        sid = service.Zaloguj(settings.REGON_API_KEY)

        # Create new authenticated session
        session = Session()
        session.headers.update({"sid": sid})

        # Create authenticated client
        client = Client(
            wsdl=self.wsdl,
            transport=Transport(
                session=session,
                timeout=3,
                operation_timeout=3,
            ),
        )

        return self._create_service(client)

    def logout_service(self, service):
        """Logout REGON service"""
        try:
            service.Wyloguj()
        except Exception as exception:
            pass  # we don't care

    def get_application_autocomplete(
        self, nip: str
    ) -> RegonAutocompleteResponse:
        """Get autocomplete data based on NIP number"""
        nip = nip.replace(" ", "").replace("-", "")
        if not validate_nip(nip):
            return RegonAutocompleteResponse(
                success=False,
                error="Wprowadzony NIP jest niepoprawny",
                company=None,
            )

        service = self.create_authenticated_service()

        xml_data = service.DaneSzukajPodmioty(
            pParametryWyszukiwania={"Nip": nip}
        )

        # Parse the XML data
        # pylint: disable=c-extension-no-member
        root = etree.fromstring(xml_data)  # type: ignore

        company: Optional[RegonCompany] = None

        for _ in root.findall("dane"):
            silos = _.find("SilosID").text
            if silos not in ["1", "6"]:
                continue

            # Property number
            property_number = _.find("NrNieruchomosci").text

            # Address
            address = f"{_.find('Ulica').text} {property_number}"
            apartment_number = _.find("NrLokalu").text
            if apartment_number:
                address = f"{address}/{apartment_number}"

            company = RegonCompany(
                nip=nip,
                name=_.find("Nazwa").text,
                address=address,
                postal_code=_.find("KodPocztowy").text,
                city=_.find("Miejscowosc").text,
            )
            break

        self.logout_service(service)

        return RegonAutocompleteResponse(
            success=bool(company),
            error="" if company else "Wprowadzony NIP jest niepoprawny",
            company=company,
        )
