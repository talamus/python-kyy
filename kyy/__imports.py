import sys
import tokenize
from enum import Enum
import black
from voikko.libvoikko import Voikko
from .error import ERROR
from .lexicon import LEXICON

Case = Enum("Case", ["TITLE", "LOWER", "UPPER", "MIXED"])

try:
    VOIKKO = Voikko("fi")
except Exception as error:
    ERROR(f"Unable to initialize Voikko: {error}")
