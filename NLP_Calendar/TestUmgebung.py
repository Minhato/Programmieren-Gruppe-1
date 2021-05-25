from numpy import empty
import spacy
from spacy.matcher import PhraseMatcher

nlp=spacy.load("de_core_news_sm")


matcher=PhraseMatcher(nlp.vocab)
term = ["titel"]
patterns = [nlp.make_doc(text) for text in term]
print(patterns)
matcher.add("titel", patterns)
titel = None
doc = nlp("Erstelle ein Termin um 15 Uhr mit dem x ich muss kacken")
matches = matcher(doc)
print(matches)

for match_id, start, end in matches:
    titel = doc[end:len(doc)]
    print(titel.text)

if not matches:
    print("Keinen Titel gefunden was wollen Sie als Titel haben?")
    #input bla bla into Titel

def getTitel():
    # Rule based wo man den alles nach "Mit dem Titel" als Titel nimmt, evtl Intent am Ende entfernen
    # wenn kein titel gefunden, dann nochmal nachfragen was titel sein soll und das dann nutzen
    # PHRASE Matcher anschauen, das wahrscheinlich sinnvoller
    # TO:DO 
    
    pass


def getTitel():
    # Rule based wo man den alles nach "Mit dem Titel" als Titel nimmt, evtl Intent am Ende entfernen
    # wenn kein titel gefunden, dann nochmal nachfragen was titel sein soll und das dann nutzen
    # PHRASE Matcher anschauen, das wahrscheinlich sinnvoller

    matcher=PhraseMatcher(nlp.vocab)
    term = ["titel"]
    patterns = [nlp.make_doc(text) for text in term]
    print(patterns)
    matcher.add("titel", patterns)
    titel = None
    doc = nlp("Erstelle ein Termin um 15 Uhr mit dem x ich muss kacken")
    matches = matcher(doc)
    print(matches)

    for match_id, start, end in matches:
        titel = doc[end:len(doc)]
        print(titel.text)

    if not matches: 
        print("Keinen Titel gefunden was wollen Sie als Titel haben?")
        #input bla bla into Titel


