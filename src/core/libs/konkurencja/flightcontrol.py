"""Flight Control"""

# flake8: noqa=E501
# pylint: disable=broad-exception-raised

from typing import Callable

from .abstracts import KonkurencjaFetcher
from .centrum_verte import CentrumVerteFetcher
from .izbapodatkowa import IzbaPodatkowaFetcher
from .jgt import JgtFetcher

KONKURENCJA_FETCHERS: dict[str, tuple[str, Callable[[str], KonkurencjaFetcher]]] = {
    "CentrumVerte": ("centrumverte.pl/szkolenia-online", CentrumVerteFetcher),
    "JGT.pl": ("jgt.pl/szkolenia", JgtFetcher),
    "IzbaPodatkowa.pl": ("izbapodatkowa.pl/szkolenie", IzbaPodatkowaFetcher),
}


def konkurencja_fetcher(url: str) -> tuple[str, KonkurencjaFetcher]:
    """konkurencja_fetcher"""

    fetcher: KonkurencjaFetcher | None = None

    for konkurencja_name, konkurencja_tuple in KONKURENCJA_FETCHERS.items():
        url_fragment, FetcherFunc = konkurencja_tuple
        konkurencja = konkurencja_name
        if url_fragment in url:
            fetcher = FetcherFunc(url)

    if fetcher is None:
        raise Exception("No fetcher found for given url")

    fetcher.initialize()

    return konkurencja, fetcher
