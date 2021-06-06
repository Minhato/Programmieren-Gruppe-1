from KalenderMethoden import terminAnlegen
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy import displacy
from datetime import*
from re import*

#Korpus laden
nlp=spacy.load("de_core_news_sm")
matcher=Matcher(nlp.vocab)

text="Lege einen Termin für Dienstag um 14 Uhr bis 14:30 mit dem Titel Hallo an"
#text = ""
text=text+"."
#Doc ist text als Spacy Doc Objekt
doc =  nlp(text)
bereinigt=" ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

#Doc mit entfernten Stopwords
noStopwordDoc=nlp(bereinigt)

tokenListe=[]

def setText(eingabe):
    global text, doc, bereinigt 
    text = eingabe
    text=text+"."
    #Doc ist text als Spacy Doc Objekt
    doc =  nlp(text)
    bereinigt=" ".join([token.text for token in doc if not token.is_stop and not token.is_punct])



def getTokenList():
    #Liste mit Tokens zum checken
    for token in noStopwordDoc:
        if(token.is_stop == False or token.pos_=="NOUN"):
            tokenListe.append(token.lemma_)
    print(tokenListe)
    
def checkActionKind():
    for token in noStopwordDoc:
        if(token.pos_=="NOUN"):
            if(token.text=="Kalender"):
                return "Kalender"
            if(token.text=="Termin"or"Meeting"or"Treffen"):
                return "Termin"
            if(token.text=="Geburtstag"):
                return"Geburtstag"

def getIntend(userInput,kindOfRequest):
    matcher=Matcher(nlp.vocab)
    #List of Intends für mögliche aktionen für den matcher.
    listOfIntends=["anlegen","löschen","ändern","verschieben","verlegen","eintragen","erstellen","Lege","Ändere","Lösche","Erstelle","Verschiebe","Verlege"]
    #Pattern anlegen
    patterns=[
        [{"TEXT":"Erstelle"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Trage"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Ändere"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Lösche"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Lege"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Verschiebe"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"TEXT":"Verlege"},{"POS":"DET"},{"TEXT":kindOfRequest}],
        [{"POS":"VERB"},{"IS_PUNCT":True}],
        [{"TEXT":kindOfRequest},{"POS":"VERB"}]
    
    ]
    
    matcher.add("Intention",patterns)
    testDoc= nlp(userInput)
    matches= matcher(testDoc)

    for match_id,start, end in matches:
   
        string_id=nlp.vocab.strings[match_id]
        span=testDoc[start:end]
        intend=span.text.replace(kindOfRequest,"").replace(" ","").replace(".","")
        if(intend in listOfIntends or len(intend)>7):
            if "lege"in intend.lower() or "erstelle"in intend.lower() or"trage"in intend.lower():
                print("Termin erstellen als Intend")
                return "erstellen"
            elif "änder" in intend.lower():
                print("Termin ändern als Intend")
                return "aendern"
            elif "lösche"in intend.lower():
                print("Termin löschen als Intend")
                return "loeschen"
            elif "verschiebe"in intend.lower() or "verlege" in intend.lower():
                print("Termin verschieben als Intend")
                return "verschiebe"







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

def getDatum(erkannterTag):
    #heutigesDatum
    heute=date.today()
    #globale Variable datumNextWeek in die Ergebis der Methode getDateNextWeek gespeichert wird,die in der for schleife der erkannten patterns aufgerufen wird
    datumNextWeek=date.today()
    #aus Parameter wird NLP objekt erstellt
    datumNlp =nlp(erkannterTag)
    #patterns
    patterns=[
        [{"LEMMA":"nächst"},{"TEXT":"Woche","OP":"?" },{"TEXT":{"REGEX":"\w*tag\b"}}],
        [{"LEMMA":"nächst"},{"TEXT":"Woche","OP":"?" },{"TEXT":"Mittwoch"}]
        
        
    ]
    #Matcher wird inizialisiert
    matcher.add("Weekdays",patterns)
    testDoc= nlp(erkannterTag)
    matches= matcher(testDoc)
    
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
    #Methode getDateNextWeek wird aufgerufen wenn pattern gematched wird
    def getDateNextWeek(spanText):
        WeekdayNextWeek = spanText.replace("nächsten","").replace("nächste","").replace("Woche","").replace(" ","")
        if(heute.weekday()<=possibleDate[WeekdayNextWeek].weekday()):
            return possibleDate[WeekdayNextWeek]+timedelta(days=7)
        else:
            return possibleDate[WeekdayNextWeek]
    
    #for Schleife die für Pattern match getDateNextWeek aufruft
    
    for match_id,start,end in matches:
        string_id=nlp.vocab.strings[match_id]            
        span=testDoc[start:end]
        print(span.text,match_id,start)
        datumNextWeek=getDateNextWeek(span.text)
    
    
    
    #return der getDatum Methode
    #deutsches Datum->return des Formatieren Datums
    #Leeres Array==Kein Pattern gefunden->normaler aufruf über dictonary
    #else->Aufruf der globalen Variable datumNextWeek in die Datum für die nächste Woche gespeichert wurde
    for token in datumNlp:
        if token.shape_=="dd.dd.dddd":
            #Platz zum formatieren des Datums zum google api Standart
            return token.text
    if(matches==[]):
        
        return possibleDate.get(erkannterTag)
    else:
        return datumNextWeek

def getDateText(userText):
    doc=nlp(userText)
    Wochentage=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    MonateValue={
        "Jannuar":"01",
        "Februar":"02",
        "März":"03",
        "April":"04",
        "Mai":"05",
        "Juni":"06",
        "Juli":"07",
        "August":"08",
        "September":"09",
        "Oktober":"10",
        "November":"11",
        "Dezember":"12"
    }
    userDatum =""
    for token in doc:
        if token.shape_=="dd."or token.shape_=="d." and token.head.text in MonateValue:
            tag=token.text
            if token.shape_=="d.":
                tag="0"+tag
            monat=MonateValue[token.head.text]
            jahr=datetime.now().year
            userDatum=tag+monat+"."+str(jahr)
            return str(userDatum)
        elif token.shape_=="dd.dd.dddd":
            userDatum=token.text
            return str(token.text)
        elif token.lemma_=="nächst" or token.text=="Woche":
            userDatum=" ".join([userDatum,token.text])
        elif token.text in Wochentage:
            userDatum=" ".join([userDatum,token.text])
            if(len(userDatum)<10):
                userDatum=userDatum[1:]
            return str(userDatum)


 

def getLocation():
    #UNFINISHED Soll Location des Termins Liefern falls Vorhanden
    for ent in doc.ents:
        print(ent.text,ent.label_)
        if(ent.label_ == "LOC"):
            return ent.text
            print("Der Termin soll hier stattfinden"+ent.text)
            

def getTitel(text):
    matcher=PhraseMatcher(nlp.vocab)
    term = ["titel"]
    patterns = [nlp.make_doc(text) for text in term]
    print(patterns)
    matcher.add("titel", patterns)
    titel = None
    doc = nlp(text)
    lower_doc =  str(doc).lower()
    matches = matcher(nlp(lower_doc))
    print(matches, "type", type(matches))

    for match_id, start, end in matches:
        print(match_id,start,end)
        titel = doc[end:len(doc)]
        print(titel.text)
        return titel

    if not matches: 
        print("Keinen Titel gefunden was wollen Sie als Titel haben?")
        #input bla bla into Titel
getTitel("erstelle einen Termin um 14 Uhr mit dem Titel Hallo was geht ab")


def getUhrzeit(index):
    uhrzeiten= []
    for token in doc:
        print(token.shape_)

        if token.shape_ == "dd":
            tokendd = str(token.text) + ":00"
            uhrzeiten.append(tokendd)

        elif token.shape_ == "dd:dd":
            uhrzeiten.append(token.text)
            
            print("ja existiert", token.text)
    print(uhrzeiten)
    print("COUNT "+ str(len(uhrzeiten)))
    if len(uhrzeiten) == 1:
        enduhrzeit = uhrzeiten[0]
        enduhrzeit = datetime.strptime(enduhrzeit, '%H:%M').replace(second=0) + timedelta( minutes= 30)
        print(str(enduhrzeit) + " die enduhrzeit bisher")
        enduhrzeit = enduhrzeit.time()
        uhrzeiten.append(str(enduhrzeit))
        print("Die enduhrzeit " +str(enduhrzeit))
        print(uhrzeiten)
    return uhrzeiten[index]

setText("Erstelle einen Termin um 14 Uhr mit dem Titel JOO")
print("gesezter Text " + text )
print("das ist die Uhrzeit " + getUhrzeit(0))

def kalenderEintrag(self):
    if self.intend is "erstellen":
        terminAnlegen(self.datum)


class Logik(object):
    def __init__(self,titel):
        self.titel = titel
    def __init__(self) -> None:
        super().__init__()


p = Logik()
p.titel = getTitel("erstelle einen Termin um 14 Uhr mit dem Titel Hallo was geht ab")
print("Objekt", p.titel)
p.datum = getIntend("erstelle einen Termin um 14 Uhr mit dem Titel Hallo was geht ab ",checkActionKind()) 


#getUhrzeit()
 #UserEvent checkt welche Infos vom User schon gegeben wurden           
# userEvent={
#     "eventKind" : checkActionKind(),
#     "intend" : getIntend(checkActionKind()),
#     "Datum":getDatum(),
#     "Zeit":"testZeit",
#     "Ort": getLocation(),
#     "Aktivität":"Testaktivität",
#     "Erinnerung":True,
# }
