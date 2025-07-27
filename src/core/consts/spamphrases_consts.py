"""
Spam and spam-forbidden phrases
"""

FORBIDDEN_PHRASES = {
    # A
    # B
    "bezpłat": True,
    # C
    "credit": True,
    "cash": True,
    # D
    "darmo": True,
    # E
    # F
    "free": True,
    # G
    # H
    # I
    # J
    # K
    "kredyt": True,
    # L
    "life": True,
    # M
    "mortgage": True,
    # N
    # O
    # P
    "pożyczk": True,
    # R
    # S
    # T
    # U
    # W
    # X
    # Y
    # Z
    "zarabia": True,
}

# ONLY SINGLE WORDS !
SPAM_PHRASES = {
    # A
    # B
    "bonus": "bon,us",
    "bezpłatna": "bezpł;atna",
    "bezpłatny": "bezpł;atny",
    # C
    "celu": "ce;lu",
    # D
    "dyrektyw": "dyre;ktyw",
    "danych": "dany;ch",
    "dofinansowania": "dofinan;sowania",
    # E
    # F
    "finanse": "fin;anse",
    "finansowych": "fina;nsowych",
    "finansowanych": "finan;sowanych",
    "finansowane": "finan;sowane",
    "finansów": "finan;sów",
    # G
    # H
    # I
    "informac": "inf;ormac",
    "inter;netowej": "inter;netowej",
    "inter;netowa": "inter;netowa",
    # J
    # K
    # "kurs": "ku;rs",
    # L
    # M
    "musisz": "mus;isz",
    # N
    "nabyć": "na;być",
    "nabycia": "na;bycia",
    "nabycie": "na;bycie",
    "podstawie": "pods;tawie",
    # O
    "osobow": "osob;ow",
    "osobowych": "osob;owych",
    "osobowych,": "osob;owych,",
    "osobowe": "osob;owe",
    "osobowe,": "osob;owe,",
    # P
    "publicz": "pub;licz",
    "publicznych": "pub;licznych,",
    "publicznych,": "pub;licznych,",
    "propozycj": "pro;pozycj",
    "przedsiębior": "przed;siębior",
    "przedsiębiorstw": "przed;siębiorstw",
    "pobrany": "pob;rany",
    # R
    "rezygnacja": "rezyg;nacja",
    "rezygnacji": "rezyg;nacji",
    # S
    "szkolen": "szko;len",
    "szkoleń": "szko;leń",
    "szczegółow": "szcze;gółow",
    "szkolenia": "szko;lenia",
    "szkoleniach": "szko;leniach",
    "szkoleniowych": "szko;leniowych",
    "szkoleniu": "szko;leniu",
    # T
    # U
    # W
    "wyrażenie": "wyra;żenie",
    "warsztat": "warsz;tat",
    # X
    # Y
    # Z
    "związku": "zwią;zku",
    "zgoda": "zgo;da",
    "Zgoda": "Zgo;da",
    "zgody": "zgo;dy",
    # !@#
    "!!!!": "!",
    "!!!": "!",
    "!!": "!",
}


# "wyrażenie zgody": "",
# "odebrać": "",
# "tylko do": "",
# "rezygnacja": "",
# "warsztaty": "",
# "do których należy się przygotować": "",
# "chcemy": "chc#emy",
# "dla firm": f"dla_firm",
# "dyrektywa": f"dyre#ktywa",
# "dyrektywy": f"dyre#ktywy",
# "danych osobowych": f"danych_osobowych",
# "dane osobowe": f"dane_osobowe",
# "kliknij": f"kli#knij",
# "kliknąć": f"kli#knąć",
# "kliknięcie": f"kli#knięcie",
# "nie chcę": f"nie_chcę",
# "na podstawie": f"na podst#awie",
# "na, podstawie": f"na, podst#awie",
# "nie stanowi": f"nie_stanowi",
# "nabycie": f"nab#ycie",
# "oferta": f"ofe#rta",
# "oferty": f"ofe#rty",
# "powyższa wiadomość": f"powyższa_wiadomość",
# "problemy": f"prob#lemy",
# "problemów": f"prob#lemów",
# "problemami": f"prob#lemami",
# "problematyka": f"prob#lematyka",
# "problem": f"prob#lem",
# "promocja": f"pro#mocja",
# "promocją": f"pro#mocją",
# "promocje": f"pro#mocje",
# "promocji": f"pro#mocji",
# "refund": f"ref#und",
# "szkoleniowe": f"szko#leniowe",
# "szkoleniowymi": f"szko#leniowymi",
# "szkoleniowym": f"szko#leniowym",
# "szkoleniowych": f"szko#leniowych",
# "szkoleniową ": f"szko#leniową",
# "szkolenie": f"szko#lenie",
# "szkolenia": f"szko#lenia",
# "szkoleniu": f"szko#leniu",
# "szkoleniowo": f"szko#leniowo",
# "szkoleniem": f"szko#leniem",
# "szkoleń": f"szk#oleń",
# "tutaj": f"tu#taj",
# "związku": "zwi#ązku",
