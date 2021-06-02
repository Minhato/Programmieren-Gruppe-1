import spacy
from spacy.lang.de.examples import sentences
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy

nlp = spacy.load("de_core_news_sm") #de_dep_news_trf für accuracy aber arsch langsam

doc = nlp("Guten Tag Dokument! lege neues Termin im Kalender an und esse")
print(doc)
for token in doc:
    print(token.text, token.pos_, token.dep_, token.lemma   )
doc_lemma = []
for mail in doc:
     result = ' '.join([x.lemma_ for x in doc]) 
doc_lemma.append(result)
print(doc_lemma)