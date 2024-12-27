"""Flight Control"""

# pylint: disable=broad-exception-raised

from .abstracts import KonkurencjaFetcher
from .centrum_verte import CentrumVerteFetcher
from .izbapodatkowa import IzbaPodatkowaFetcher
from .jgt import JgtFetcher


def konkurencja_fetcher(url: str) -> tuple[str, KonkurencjaFetcher]:
    """konkurencja_fetcher"""

    fetcher: KonkurencjaFetcher | None = None

    if "centrumverte.pl/szkolenia-online" in url:
        konkurencja = "CentrumVerte"
        fetcher = CentrumVerteFetcher(url)
    elif "jgt.pl/szkolenia" in url:
        konkurencja = "JGT.pl"
        fetcher = JgtFetcher(url)
    elif "izbapodatkowa.pl/szkolenie" in url:
        konkurencja = "IzbaPodatkowa.pl"
        fetcher = IzbaPodatkowaFetcher(url)
    else:
        raise Exception("No fetcher found for given url")

    fetcher.initialize()

    return konkurencja, fetcher
