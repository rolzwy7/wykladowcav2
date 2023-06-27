from django.conf import settings
from lxml import etree
from requests import Session
from rest_framework.decorators import (
    api_view,
    renderer_classes,
    throttle_classes,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from zeep import Client
from zeep.transports import Transport

from api.base.throttling import RegonAutocompleteThrottle
from core.libs.validators.nip_validator import validate_nip

# TODO: This shouldn't be in controller
# movie this to separate service


@api_view(["POST"])
@renderer_classes([JSONRenderer])  # policy decorator
@throttle_classes([RegonAutocompleteThrottle])
def regon_autocomplete(request):
    """Return company data from REGON"""

    if not validate_nip(request.data["nip"]):
        return Response(
            {"success": False, "error": "Wprowadzony NIP jest niepoprawny"}
        )

    wsdl = (
        "https://wyszukiwarkaregon.stat.gov.pl"
        "/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-prod.wsdl"
    )
    service_url = (
        "https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc"
    )
    namespace = "{http://tempuri.org/}e3"

    def create_service(client: Client):
        return client.create_service(
            namespace,
            service_url,
        )

    client = Client(wsdl=wsdl)
    service = create_service(client)

    sid = service.Zaloguj(settings.REGON_API_KEY)
    session = Session()
    session.headers.update({"sid": sid})

    client = Client(
        wsdl=wsdl,
        transport=Transport(
            session=session,
            timeout=3,
            operation_timeout=3,
        ),
    )
    service = create_service(client)

    xml_data = service.DaneSzukajPodmioty(
        pParametryWyszukiwania={"Nip": request.data["nip"]}
    )

    # Parse the XML data
    root = etree.fromstring(xml_data)  # type: ignore

    companies = []
    for dane_element in root.findall("dane"):
        silos = dane_element.find("SilosID").text
        if silos not in ["1", "6"]:
            continue
        name = dane_element.find("Nazwa").text
        nip = dane_element.find("Nip").text
        city = dane_element.find("Miejscowosc").text
        postal_code = dane_element.find("KodPocztowy").text
        street = dane_element.find("Ulica").text

        property_number = dane_element.find("NrNieruchomosci").text
        address = f"{street} {property_number}"
        apartment_number = dane_element.find("NrLokalu").text
        if apartment_number:
            address = f"{address}/{apartment_number}"

        companies.append(
            {
                "nip": nip,
                "name": name,
                "address": address,
                "postal_code": postal_code,
                "city": city,
            }
        )

    service.Wyloguj()

    if len(companies) > 0:
        return Response({"success": True, "data": companies[0]})
    else:
        return Response(
            {
                "success": False,
                "error": "Brak wyników w REGON dla danego numeru NIP",
            }
        )
