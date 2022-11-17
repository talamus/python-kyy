KYY_TO_PYTHON = {
    ("tulostaa_teonsana",): "print",                # tulosta() -> print()
    ("jokainen_laatusana",): "for",                 # jokaiselle -> for
    ("joka_asemosana", "löytyä_teonsana",): "in",   # joka löytyy -> in
    ("jos_sidesana",): "if",                        # jos -> if
    ("muuten_seikkasana",): "else",                 # muuten -> else
    ("numeroitu_laatusana",): "enumerate",          # numeroidusta -> enumerate
    ("numeroitu_laatusana_plural",): "enumerate",   # numeroiduista -> enumerate
    ("aliohjelma",): "def",                         # aliohjelma -> def
    ("luokka",): "class",                           # luokka -> class
    # To be continued...
}

# Parse into a dictionary for easier referencing
LEXICON = dict()
for kyy, python in KYY_TO_PYTHON.items():
    LEXICON[kyy[0]] = {"kyy": kyy, "python": python}
