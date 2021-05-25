import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy import displacy
from datetime import*
from re import*

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







def calculateWithWeekdays(requestedWeekday):
    """Gibt für einen gewünschten Wochentag das entsprechende Datum zurück"""
    #Wochentag zum iterieren über die while Schleife
    weekdayToday=date.weekday(date.today())
    calculatedDate=date.today()
    #statisches Startdatum
    startDatum=date.weekday(date.today())

    while(weekdayToday != requestedWeekday):
        
        calculatedDate=calculatedDate+timedelta(days=1)
        
        weekdayToday=date.weekday(calculatedDate)
    return calculatedDate

def getDatum(regognizedDay):
    """Verarbeitet vom Nutzer eingegebenen Text der sich auf das Datum bezieht und gibt errechnetes Wunschdatum zurück"""
    #heutigesDatum
    heute=date.today()
    #globale Variable datumNextWeek in die Ergebis der Methode getDateNextWeek gespeichert wird,die in der for schleife der erkannten patterns aufgerufen wird
    datumNextWeek=date.today()
    #patterns
    patterns=[
        [{"LEMMA":"nächst"},{"TEXT":"Woche","OP":"?" },{"TEXT":{"REGEX":"\w*tag\b"}}],
        [{"LEMMA":"nächst"},{"TEXT":"Woche","OP":"?" },{"TEXT":"Mittwoch"}]
        
        
    ]
    #Matcher wird inizialisiert
    matcher.add("Weekdays",patterns)
    testDoc= nlp(regognizedDay)
    matches= matcher(testDoc)

    #Dictonary zur Abrage des Datums je nach Case
    possibleDate={
        "heute":heute,
        "morgen":heute+timedelta(days=1),
        "übermorgen":heute+timedelta(days=2),
        "Montag":calculateWithWeekdays(0),
        "Dienstag":calculateWithWeekdays(1),
        "Mittwoch":calculateWithWeekdays(2),
        "Donnerstag":calculateWithWeekdays(3),
        "Freitag":calculateWithWeekdays(4),
        "Samstag":calculateWithWeekdays(5),
        "Sonntag":calculateWithWeekdays(6)
    }
    #Methode getDateNextWeek wird aufgerufen wenn pattern gematched wird,manipuliert wenn nötig Dictonaryabfrage um 7
    def getDateNextWeek(spanText):
        WeekdayNextWeek = spanText.replace("nächsten","").replace("nächste","").replace("Woche","").replace(" ","")
        if(heute.weekday()<=possibleDate[WeekdayNextWeek].weekday()):
            return possibleDate[WeekdayNextWeek]+timedelta(days=7)
        else:
            return possibleDate[WeekdayNextWeek]
    
    #for Schleife die für Pattern match getDateNextWeek aufruft und globaler Variable datumNextWeek zuweißt
    
    for match_id,start,end in matches:
        string_id=nlp.vocab.strings[match_id]            
        span=testDoc[start:end]
        print(span.text,match_id,start)
        datumNextWeek=getDateNextWeek(span.text)
    
    
    #return der getDatum Methode
    #Leeres Array==Kein Pattern gefunden->normaler aufruf über dictonary
    #else->Aufruf der globalen Variable datumNextWeek in die Datum für die nächste Woche gespeichert wurde
    if(matches==[]):
        return possibleDate.get(regognizedDay)
    else:
        return datumNextWeek
   
        
    
            
print(getDatum("nächste Woche Freitag"))


 

def getLocation():
    #UNFINISHED Soll Location des Termins Liefern falls Vorhanden
    for ent in doc.ents:
        print(ent.text,ent.label_)
        if(ent.label_ == "LOC"):
            return ent.text
            print("Der Termin soll hier stattfinden"+ent.text)
            

def getTitel():
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