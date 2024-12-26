"""Flight Control"""

# pylint: disable=broad-exception-raised

from .abstracts import KonkurencjaFetcher
from .centrum_verte import CentrumVerteFetcher


def konkurencja_fetcher(url: str) -> KonkurencjaFetcher:
    """konkurencja_fetcher"""

    fetcher: KonkurencjaFetcher | None = None

    if "centrumverte.pl/szkolenia-online/" in url:
        fetcher = CentrumVerteFetcher(url)
    else:
        raise Exception("No fetcher found for given url")

    fetcher.initialize()

    return fetcher
