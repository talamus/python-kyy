KYY_TO_PYTHON = {
    ("tulostaa_teonsana",): "print",
    ("jokainen_laatusana",): "for",
    ("joka_asemosana", "löytyä_teonsana",): "in",
    ("jos_sidesana",): "if",
    ("muuten_seikkasana",): "else",
    ("lista",): "list",
    ("numeroitu_laatusana_plural",): "enumerate",
}

# Parse into a dictionary for easier referencing
LEXICON = dict()
for kyy, python in KYY_TO_PYTHON.items():
    LEXICON[kyy[0]] = {"kyy": kyy, "python": python}
