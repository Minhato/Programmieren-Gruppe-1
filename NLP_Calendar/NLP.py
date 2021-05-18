import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy import displacy
from datetime import*

#Korpus laden
nlp=spacy.load("de_core_news_sm")
matcher=Matcher(nlp.vocab)


text="Hier steht unser Testsatz"
bereinigt=" ".join([token.text for token in doc if not token.is_stop and not token.is_punct])
#Doc ist text als Spacy Doc Objekt
doc =  nlp(text)
#Doc mit entfernten Stopwords
noStopwordDoc=nlp(bereinigt)

tokenListe=[]
def getTokenList():
    #Liste mit Tokens zum checken
    for token in noStopwordDoc:
        if(token.is_stop == False or token.pos_=="NOUN"):
            tokenListe.append(token.lemma_)
    print(tokenListe)
    
    
def checkActionKind():
    #Dursucht Satz nach Entität für Art der Anlage
    for token in noStopwordDoc:
        
        
        if(token.pos_=="NOUN"):
            if(token.text=="Kalender"):
                return "Kalender"
            if(token.text=="Termin"or"Meeting"or"Treffen"):
                return "Termin"
            if(token.text=="Geburtstag"):
                return"Geburtstag"

def getIntend(kindOfRequest):
    matcher=Matcher(nlp.vocab)
    #List of Intends für mögliche aktionen für den matcher.
    listOfIntends=["anlegen","löschen","ändern","eintragen","erstellen","Lege","Ändere","Lösche","Erstelle"]
    #Pattern anlegen
    patterns=[
        [{"TEXT":"Erstelle"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Trage"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Ändere"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Lösche"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Lege"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"POS":"VERB"},{"IS_PUNCT":True}],
        [{"TEXT":kindOfRequest},{"POS":"VERB"}]
    
    ]
    
    matcher.add("Intention",patterns)
    testDoc= nlp("Lege einen Termin an mit dem Titel:Daan geht um 7 Uhr seinen dust löschen.")
    matches= matcher(testDoc)

    for match_id,start, end in matches:
   
        string_id=nlp.vocab.strings[match_id]
        span=testDoc[start:end]
        intend=span.text.replace(kindOfRequest,"").replace(" ","").replace(".","")
        if(intend in listOfIntends or len(intend)>7):
            if "lege"in intend.lower() or "erstelle"in intend.lower() or"trage"in intend.lower():
                print("Termin erstellen als Intend")
            elif "änder" in intend.lower():
                print("Termin ändern als Intend")
            elif "lösche"in intend.lower():
                print("Termin löschen als Intend")




def getLocation():
    #UNFINISHED Soll Location des Termins Liefern falls Vorhanden
    for ent in doc.ents:
        print(ent.text,ent.label_)
        if(ent.label_ == "LOC"):
            return ent.text
            print("Der Termin soll hier stattfinden"+ent.text)
            
def getDatum():
    #UNFINISHED Soll Datum des Termins liefern
    today = date.today()
    for token in doc:
        if(token.text=="heute"):
            return str(today)





 #UserEvent checkt welche Infos vom User schon gegeben wurden           
userEvent={
    "eventKind" : checkActionKind(),
    "intend" : getIntend(checkActionKind()),
    "Datum":getDatum(),
    "Zeit":"testZeit",
    "Ort": getLocation(),
    "Aktivität":"Testaktivität",
    "Erinnerung":True,
}