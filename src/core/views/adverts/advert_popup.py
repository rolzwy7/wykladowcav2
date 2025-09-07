# flake8: noqa
# pylint: disable=unused-import

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

# Zakładając, że poniższe modele znajdują się w pliku models.py w tej samej aplikacji
from core.libs.spy import create_spy_object
from core.models import AdvertPopup, AdvertPopupClick


def advert_popup_track_click(request: HttpRequest, uuid: str) -> HttpResponseRedirect:
    """
    Rejestruje kliknięcie w popup i przekierowuje użytkownika do docelowego adresu URL.

    Args:
        request: Obiekt HttpRequest.
        uuid: UUID popupu, który został kliknięty.

    Returns:
        Przekierowanie (HttpResponseRedirect) do target_url z obiektu AdvertPopup.
        Zwraca 404, jeśli popup o danym ID nie istnieje lub nie jest aktywny.
    """
    # Używamy menedżera .manager.get_active(), aby upewnić się,
    # że zliczamy kliknięcia i przekierowujemy tylko dla aktywnych popupów.
    # get_object_or_404 automatycznie obsłuży błąd, jeśli popup nie zostanie znaleziony.
    popup = get_object_or_404(AdvertPopup.manager.get_active(), pk=uuid)

    # Tworzymy nowy wpis w bazie danych, aby zarejestrować kliknięcie.
    # Pole spy_object jest opcjonalne, więc na razie go pomijamy.
    # W bardziej rozbudowanej aplikacji moglibyśmy tu powiązać kliknięcie
    # z sesją użytkownika lub innym obiektem śledzącym.

    spy_object = create_spy_object(request, "ADVERT_POPUP_CLICK")

    AdvertPopupClick(popup=popup, spy_object=spy_object).save()

    # Przekierowujemy użytkownika na docelowy adres URL zdefiniowany w popupie.
    return redirect(popup.target_url)
