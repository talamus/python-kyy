from .__imports import *


class Name:
    """Convert NAME token into a named entity."""

    original_token: tokenize.TokenInfo
    only_lemma: str | None
    lemmas: set[str]
    command: None | dict

    def __init__(self, token: tokenize.TokenInfo) -> None:
        """Convert NAME token into a named entity."""
        if token.type != tokenize.NAME:
            raise TypeError("Token type has to be NAME", token)
        self.original_token = token
        self.analyzis = VOIKKO.analyze(token.string)

        # Reduce to basic forms
        lemmas = set()
        only_lemma = None
        for word in self.analyzis:
            lemma = word["BASEFORM"]
            if "CLASS" in word and word["CLASS"] != "nimisana":
                lemma += "_" + word["CLASS"]
            if "NUMBER" in word and word["NUMBER"] == "plural":
                lemma += "_plural"
            lemmas.add(lemma)
            only_lemma = lemma
        self.lemmas = lemmas
        if len(lemmas) == 1:
            self.only_lemma = only_lemma
        else:
            self.only_lemma = None

        # Mark as a (potential) command if found in Kyy language lexicon
        self.command = None
        for lemma in lemmas:
            if lemma in LEXICON:
                self.command = LEXICON[lemma]
                break

    def __str__(self):
        if self.only_lemma:
            return self.only_lemma
        else:
            return str(self.lemmas)
