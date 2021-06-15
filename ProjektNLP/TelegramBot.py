#from NLP_Calendar.Logik import Logik
from typing import no_type_check
import telebot
import spacy
from  Logik import *
from telebot import types

#Boolean zum überprüfen der ersten Nachricht
ersteUserNachricht=True
#TheBotler
tokenAPI = '1816801935:AAHAH98soREBBJvN2MQOAT4FaaCByDevG9w'
pp = Logik()
#Emojii register
labCoat = u'\U0001F97C' 
robot= u'\U0001F916'


bot = telebot.TeleBot(tokenAPI)
#Commands
@bot.message_handler(commands=['start'])
def echo_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und verwaltet Ihren Terminkalender\nmit'/help' erhalten Sie eine genauere Beschreibung des Botlers.\nMit '/commands' erhalten Sie eine ausführliche Auflistung der möglichen Aktionen und der benötigten, sowie gültigen Eingaben\n\nMöge die Organisation deiner Zeit mit dir sein!")
    bot.send_message(chat_id, "Ihr Botler wurde gestartet geben Sie einen Satz ein"+robot)
    bot.send_photo(chat_id, photo= open('Botler_farbig_start.jpg', 'rb'))
 
@bot.message_handler(commands=['help'])
def echo_message(message):
    chat_id= message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und hilft Ihnen dabei Ordnung in ihre Termine zu bringen"+robot+"\n\nMit dem Botler kannst du Google Calender Termine anlegen,anzeigen,löschen,ändern oder verschieben\n\n""Dazu kannst du einfach einen Satz schreiben, der Botler erledigt den Rest und Fragt zur Not nochmal nach.\n\n\nMit Informationen über Art des Termins,Datum,Uhrzeit und Titel des Termins bist du aber auf der sicheren Seite;)")
    bot.send_photo(chat_id, photo= open('Botler_farbig_help.jpg', 'rb'))
@bot.message_handler(commands=['commands'])
def echo_message(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,"Hier siehst du eine vollständige Auflistung aller Möglichen Aktionen des Botlers"+labCoat+
    
    """\n\nWie auch im echten Leben sind die Fähigkeiten eines B(ot)uttlers begrenzt, aber er gibt sein bestes deine Wünsche zu erfüllen.\n
    Sollte ihr Botler nicht mehr reagieren liegt ein seltener Fehler vor.
    In diesem Fall bitten wir dich die Python Datei erneut zu starten.
     Commands:

    Termin anlegen:
    benötigt Titel,Datum,Uhrzeit,intend
    
    Termin löschen:
    benötigt Datum,Uhrzeit,intend

    Termin bearbeiten:
    benötigt Datum,Uhrzeit,neuer Titel,intend

    Termin verschieben(verschiebt Termin um 2h zurück):
    benötigt
    Titel,Datum,Uhrzeit

    *Mögliche Inputs*

    Titel:
    Alles nach Keyword Titel

    Datum:
    -Datum im dd.dd.dddd Format 
    -Daten im d. oder d + Monat Format 
    -Keywords heute,morgen,übermorgen 
    -Wochentage 
    -Lemma(nächst)+(OP:Woche)+Wochentag 
    z.B(nächsten Dienstag/nächste Woche Dienstag) 

    Uhrzeit:
    -Uhrzeit in dd:dd
    -Uhrzeit in dd + Uhr

    Enduhrzeit:
    Uhrzeit - Enduhrzeit
    bis + Uhrzeit

    Intend:
    -Intend am Ende des Satzes 
    -Imperativ + DET+ ActionKind 
    -ActionKind+Intend 
    -Intend + PRON +DET+Action Kind(für anzeigen)
    -Intend als Imperativ am Anfang des Satzes

     """)
#Methoden
def checkAllInputs(userEingabe):
    setText(userEingabe)
    try:
        pp.titel = getTitel(userEingabe)
    except:
        pp.titel=None
    try:
        pp.intend =getIntend(userEingabe,checkActionKind(userEingabe))
    except:
        pp.intend=None
    try:
        pp.art = checkActionKind(userEingabe)
        print("die ART:")
        print(pp.art)
    except:
        pp.art = None
    try:
        pp.uhrzeit = getUhrzeit(0)
    except:
        pp.uhrzeit=None
    try:
        pp.enduhrzeit = getUhrzeit(1)
    except:
        pp.enduhrzeit=None
    try:
        #pp.datum=getDateText(eingabe)
        pp.datum=getDatum(getDateText(userEingabe))
    except: 
        pp.datum=None

def formatAndSendMessages(chat_id):
    """Sendet erkannte elemente an Nutzer wenn Vollständig"""
    #Nachrichten Formatieren
    chatTitel = "Titel lautet: " + str(pp.titel)
    chatUhrzeit = "Anfangsuhrzeit ist: " + str(pp.uhrzeit) + " Uhr"
    chatEndUhrzeit = "Enduhrzeit ist: " + str(pp.enduhrzeit) + " Uhr"    
    chatIntend="Erkannter intend ist: "+str(pp.intend)
    chatDatum="geplates Datum ist der: "+str(pp.datum)
    #Nachrichten an Nutzer senden
    bot.send_message(chat_id, chatTitel)
    bot.send_message(chat_id, chatUhrzeit)
    bot.send_message(chat_id, chatEndUhrzeit)
    bot.send_message(chat_id, chatIntend)
    bot.send_message(chat_id, chatDatum)

    
def missingValueNachfrage(chat_id, missingValues):
    for element in missingValues:
        if(element=='titel'):
            if(pp.intend=="bearbeiten"):
                bot.send_message(chat_id,"Wie soll der neue Titel lauten?")
            else:
                bot.send_message(chat_id,'Ich konnte aus deinem Satz leider keinen Titel erkennen\nBitte gebe einen Titel mit "Titel ist" an wie "Titel ist Skaten mit Minh')
        elif(element=='uhrzeit'):
            if(pp.intend=="bearbeiten"):
                bot.send_message(chat_id,"Um wieviel Uhr findet der Termin statt den du bearbeiten willst?")
            else:    
                bot.send_message(chat_id,"In deinem Satz ist keine Anfangsuhrzeit des Termines angegeben\nBitte gebe eine Startuhrzeit an wie z.B 15 Uhr")
        elif(element=='datum'):
            if(pp.intend=="bearbeiten"):
                bot.send_message(chat_id,"An welchem Datum ist der Termin den du bearbeiten willst?")
            else:
                bot.send_message(chat_id,"In deinem Satz ist kein Datum genannt\n Bitte gebe ein Datum an wie z.B 3. Juni/01.01.2021 oder nächsten Mittwoch")



def intendCheck(chat_id,ppDict):
    if(ppDict['intend']==None):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('zeige an')
        itembtn2 = types.KeyboardButton('erstellen')
        itembtn3 = types.KeyboardButton('bearbeiten')
        itembtn4 = types.KeyboardButton('verschiebe')
        itembtn5 = types.KeyboardButton('loeschen')
        markup.add(itembtn1, itembtn2, itembtn3,itembtn4,itembtn5)
        bot.send_message(chat_id, "Wähle einen Intent aus:", reply_markup=markup)

def checkDicForMissingValue(ppDict,intend):
    try:
        print(intend)
        if pp.art=="Termin":
            googleMethodenTermin={'erstellen':['titel','intend','uhrzeit','enduhrzeit','datum'],'zeige an':['datum'],'bearbeiten':['titel','intend','uhrzeit','enduhrzeit','datum'],'loeschen':['uhrzeit','datum'],'verschiebe':['uhrzeit','enduhrzeit','datum']}
            necessaryInput=googleMethodenTermin[intend]
        if pp.art=="Kalender":
            googleMethodenKalender={'erstellen':['titel'],'loeschen':['titel']}
            necessaryInput=googleMethodenKalender[intend]

        missingElement=[]
        print(type(missingElement))
        for element in necessaryInput:
            print(element+" for schleife Funkitioniert") 
            if(ppDict[element]==None):
                missingElement.append(element)
        return missingElement
    except:
        print("etwas ist schiefgelaufen")

def checkSpecificInput(userEingabe,chat_id):
    try:
        if pp.titel==None:
            print("Er geht in die Titel schleife rein")
            pp.titel=getTitel(userEingabe)
    except:
        pass
    try:
        if pp.intend==None:
            pp.intend=getIntend(userEingabe,checkActionKind())
    except:
        bot.send_message(chat_id,"Kein Intend erkannt, bitte erneut angeben")
    try:
        if pp.uhrzeit==None:
            pp.uhrzeit=getUhrzeit(0)
    except:
        pass
    try:
        if pp.enduhrzeit==None:
            print("enduhrzeit wird ausgeführt")
            pp.enduhrzeit=getUhrzeit(1)
    except:
        pass
    try:
        if pp.datum==None:
            pp.datum=getDatum(getDateText(userEingabe))
        
    except:
        pass

@bot.message_handler(content_types=['audio'])
def voice_handler(self):
    dateiVoice = bot._get_f



#Message Handler
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    #chatID und eingabe erfassen
    chat_id = message.chat.id
    eingabe = message.text
    setText(eingabe)
    global ersteUserNachricht
    print(ersteUserNachricht)
    intendListe={'erstellen','bearbeiten','loeschen','verschiebe','zeige an'}
    #If Abrage wird aufgeführt wenn erste user Nachricht==True->checkt alle Inputs
    if (ersteUserNachricht==True):
        #setzt alle Inputs->falls Leer ==None
        checkAllInputs(eingabe)
        print(pp.__dict__)
        #Wenn keine missing Inputs gefunden wird message gesendet und Action ausgeführt
        if(checkDicForMissingValue(pp.__dict__,pp.intend)==[]):
            formatAndSendMessages(chat_id)
            print(ersteUserNachricht)
            bot.send_message(chat_id, pp.testest())
            ersteUserNachricht=True
            return
    if pp.intend not in intendListe:
        intendCheck(chat_id,pp.__dict__)
        print(pp.__dict__)
        print(eingabe)
        print(pp.intend)
        pp.intend = eingabe
        print(pp.__dict__)
        ersteUserNachricht = False
    if pp.intend in intendListe:
        ersteUserNachricht =False
        if ersteUserNachricht == False:
            print("2.Else Schelife wurde erreicht")
            checkSpecificInput(eingabe,chat_id)
            print(pp.__dict__)
            if(checkDicForMissingValue(pp.__dict__,pp.intend)==[]):
                formatAndSendMessages(chat_id)
                bot.send_message(chat_id, pp.testest())
                ersteUserNachricht=True

        missingValueArray=checkDicForMissingValue(pp.__dict__,pp.intend)
        missingValueNachfrage(chat_id,missingValueArray)
        print(pp.__dict__)
            
        

bot.polling()
