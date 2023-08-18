# SPAM_PHRASES = {  # TODO
#     "propozycja": "",
#     "dla przedsiębiorstw": "",
#     "szczegółowe informacje": "",
#     "wyrażenie zgody": "",
#     "zgoda": "",
#     "odebrać": "",
#     "darmowe/y": "",
#     "publiczny*": "",
#     "musisz": "",
#     "finans*": "",
#     "tylko do": "",
#     "danych osobowych": "",
#     "rezygnacja": "",
#     "free": "",
#     "darmo": "",
#     "credit": "",
#     "kredyt": "",
#     "warsztaty": "",
#     "w celu": "",
#     "do których należy się przygotować": "",
#     "musisz się": "",
#     "cash": "ca#sh",
#     "credit": "cre#dit",
#     "chcemy": "chc#emy",
#     "dla firm": f"dla_firm",
#     "dyrektywa": f"dyre#ktywa",
#     "dyrektywy": f"dyre#ktywy",
#     "danych osobowych": f"danych_osobowych",
#     "dane osobowe": f"dane_osobowe",
#     "life": f"li#fe",
#     "finansowanej": f"fina#nsowanej",
#     "finansowania": f"fina#nsowania",
#     "finansowy": f"fina#nsowy",
#     "finanse": f"fina#nse",
#     "finansów": f"fina#nsów",
#     "kliknij": f"kli#knij",
#     "kliknąć": f"kli#knąć",
#     "kliknięcie": f"kli#knięcie",
#     "kredytowanie": f"kre#dytowanie",
#     "kredytów": f"kre#dytów",
#     "kredyt": f"kre#dyt",
#     "kursów": f"ku#rsów",
#     "kursy": f"ku#rsy",
#     "kurs": f"ku#rs",
#     "mortgage": "mort#gage",
#     "nie chcę": f"nie_chcę",
#     "na podstawie": f"na podst#awie",
#     "na, podstawie": f"na, podst#awie",
#     "nie stanowi": f"nie_stanowi",
#     "nabycie": f"nab#ycie",
#     "nabycia": f"nab#ycia",
#     "oferta": f"ofe#rta",
#     "oferty": f"ofe#rty",
#     "powyższa wiadomość": f"powyższa_wiadomość",
#     "problemy": f"prob#lemy",
#     "problemów": f"prob#lemów",
#     "problemami": f"prob#lemami",
#     "problematyka": f"prob#lematyka",
#     "problem": f"prob#lem",
#     "promocja": f"pro#mocja",
#     "promocją": f"pro#mocją",
#     "promocje": f"pro#mocje",
#     "promocji": f"pro#mocji",
#     "refund": f"ref#und",
#     "szkoleniowe": f"szko#leniowe",
#     "szkoleniowymi": f"szko#leniowymi",
#     "szkoleniowym": f"szko#leniowym",
#     "szkoleniowych": f"szko#leniowych",
#     "szkoleniową ": f"szko#leniową",
#     "szkolenie": f"szko#lenie",
#     "szkolenia": f"szko#lenia",
#     "szkoleniu": f"szko#leniu",
#     "szkoleniowo": f"szko#leniowo",
#     "szkoleniem": f"szko#leniem",
#     "szkoleń": f"szk#oleń",
#     "tutaj": f"tu#taj",
#     "związku": "zwi#ązku",
#     "zgoda": "zgo#da",
# }


class AntispamService:
    """Anti-Spam service"""

    def __init__(self, content: str):
        self.original_content = content
        self.content_lower = content.lower()

    @staticmethod  # TODO
    def calculate_text_html_ratio(html: str, text: str) -> float:
        """Calculate ratio between lengths of text and html content"""
        if len(html) == 0:
            return -1
        return round(len(text) / len(html), 2)

    def detect_spam_phrases(self):  # TODO: detect_spam_phrases
        """Detect spam phrases in content"""
        pass

    def calculate_spam_pharse_score(self):  # TODO: calculate
        """Calculate spam score for content"""
        pass

    def html_replace_spam_phrases(self):  # TODO: html_replace_spam_phrases
        """Replace spam phrases in HTML with replacements"""
        pass
