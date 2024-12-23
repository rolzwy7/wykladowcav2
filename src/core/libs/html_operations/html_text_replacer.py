"""HTML Text Replacer"""

# flake8: noqa=E501

import re

from bs4 import BeautifulSoup, Comment

ANTISPAM_REPLACEMENTS_MAP = {
    "bezpłat": "bezpł;at",
    "check": "",
    "danych osobowych": "dan;ych osob;owych",
    "danym osobowym": "dan;ym osob;owym",
    "danymi osobowymi": "dan;ymi osob;owymi",
    "dane osobowe": "dan;e osob;owe",
    "osobow": "osob;ow",
    "darmow": "da;rmow",
    "dyrektyw": "dyrek;tyw",
    "finans": "finan;s",
    "na podstawie": "na pods;tawie",
    "publiczn": "pub;liczn",
    "oferuje": "ofer;uje",
    "problem": "prob;lem",
    "strona internetowa": "strona intern;etowa",
    "stronie internetowej": "stronie intern;etowej",
    "strony internetowej": "strony intern;etowej",
    "szkoleni": "szko;leni",
    "uzgodnień": "uzgod;nień",
    "w temacie": "w tema;cie",
    "związku": "zwią;zku",
    "warsztat": "wars;ztat",
    "zapytanie": "zapyt;anie",
    "ze strony": "ze str;ony",
    "zgoda": "zgo;da",
    "zgodnie": "zgod;nie",
    "zrezygnować": "zrezyg;nować",
    "świadczenia usług": "świad;czenia usług",
    "świadczeniu usług": "świad;czeniu usług",
    "bonus": "bon,us",
    "celu": "ce;lu",
    "finanse": "fin;anse",
    "finansowych": "fina;nsowych",
    "finansowanych": "finan;sowanych",
    "finansowane": "finan;sowane",
    "finansów": "finan;sów",
    "informac": "inf;ormac",
    "inter;netowej": "inter;netowej",
    "inter;netowa": "inter;netowa",
    "kurs": "ku;rs",
    "musisz": "mus;isz",
    "nabyć": "na;być",
    "nabycia": "na;bycia",
    "nabycie": "na;bycie",
    "podstawie": "pods;tawie",
    "osobowych": "osob;owych",
    "osobowych,": "osob;owych,",
    "osobowe": "osob;owe",
    "osobowe,": "osob;owe,",
    "publicz": "pub;licz",
    "publicznych": "pub;licznych,",
    "publicznych,": "pub;licznych,",
    "propozycj": "pro;pozycj",
    "przedsiębior": "przed;siębior",
    "przedsiębiorstw": "przed;siębiorstw",
    "pobrany": "pob;rany",
    "rezygnacja": "rezyg;nacja",
    "rezygnacji": "rezyg;nacji",
    "szkolen": "szko;len",
    "szkoleń": "szko;leń",
    "szczegółow": "szcze;gółow",
    "szkolenia": "szko;lenia",
    "szkoleniach": "szko;leniach",
    "szkoleniowych": "szko;leniowych",
    "szkoleniu": "szko;leniu",
    "wyrażenie": "wyra;żenie",
    "zgody": "zgo;dy",
}


class HTMLTextReplacer:
    """HTMLTextReplacer"""

    def __init__(self, replacements: dict[str, str]):
        """init"""
        self.replacements = replacements

    def replace_text(self, html_content: str) -> str:
        """
        Replace text in the given HTML content based on the replacements map.
        :param html_content: A string containing HTML content.
        :return: Modified HTML content with replacements applied.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Traverse all text nodes in the HTML
        for text_node in soup.find_all(string=True):
            if isinstance(text_node, Comment):
                continue
            modified_text = text_node
            for old, new in self.replacements.items():
                # Use re.sub to replace text case insensitively
                modified_text = re.sub(
                    re.escape(old), new, modified_text, flags=re.IGNORECASE
                )
            # Replace the text node with the modified text
            text_node.replace_with(modified_text)

        # Return the modified HTML as a string
        return str(soup)
