from voikko.libvoikko import Voikko, Sentence

voikko = Voikko("fi")
text = "kysy"

for t in text.split(" "):

    analyzis = voikko.analyze(t)

    # Reduce to lemmas
    lemmas = set()
    for word in analyzis:
        lemma = word["BASEFORM"]
        if "CLASS" in word and word["CLASS"] != "nimisana":
            lemma += "_" + word["CLASS"]
        if "NUMBER" in word and word["NUMBER"] == "plural":
            lemma += "_plural"
        lemmas.add(lemma)
    print(t, "->", lemmas)
