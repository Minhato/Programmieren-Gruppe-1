
#from NLP_Calendar.Logik import Logik
import telebot
import spacy
from  Logik import *


#TheBotler
tokenAPI = '1816801935:AAHAH98soREBBJvN2MQOAT4FaaCByDevG9w'
pp = Logik()

bot = telebot.TeleBot(tokenAPI)
@bot.message_handler(commands=['start'])
def echo_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und verwaltet Ihren Terminkaländer\nmit'/help' erhalten Sie eine ausführliche beschreibung aller Funktionalitäten.\nMöge die Organisation deiner Zeit mit dir sein!")
    bot.send_message(chat_id, "Ihr Botler wurde gestartet geben Sie einen Satz ein")
    
    
    print("stratet")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    #chatID und eingabe erfassen
    chat_id = message.chat.id
    eingabe = message.text
    setText(eingabe)
    print("eingabetyp:",type(eingabe))

    #Methoden aufruf und speichern in Objekt
    try:
        pp.titel = getTitel(eingabe)
    except:
        pp.titel=None
    try:
        pp.intend =getIntend(eingabe,checkActionKind())
    except:
        pp.intend=None
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
        pp.datum=getDatum(getDateText(eingabe))
    except: 
        pp.datum=None
    

      
   

    #Bot Antwort vorbereiten
    intendCheck(chat_id,pp.__dict__)
    try:print(checkDicForMissingValue(pp.__dict__,pp.intend))
    except:print("kein Intend gefunden")
    chatTitel = "Titel lautet: " + str(pp.titel)
    chatUhrzeit = "Anfangsuhrzeit ist: " + str(pp.uhrzeit) + " Uhr"
    chatEndUhrzeit = "Enduhrzeit ist: " + str(pp.enduhrzeit) + " Uhr"    
    chatIntend="Erkannter intend ist: "+str(pp.intend)
    chatDatum="geplates Datum ist der: "+str(pp.datum)
    #Bot Antwort senden
    bot.send_message(chat_id, chatTitel)
    bot.send_message(chat_id, chatUhrzeit)
    bot.send_message(chat_id, chatEndUhrzeit)
    bot.send_message(chat_id, chatIntend)
    bot.send_message(chat_id, chatDatum)

def missingValueNachfrage(chat_id, missingValues):
    for element in missingValues:
        if(element=='titel'):
            bot.send_message(chat_id,"Ich konnte aus deinem Satz leider keinen Titel erkennen\nBitte gebe einen Titel an wie z.B Skaten mit Mihn")
        elif(element=='uhrzeit'):
            bot.send_message(chat_id,"In deinem Satz ist keine Anfangsuhrzeit des Termines angegeben\nBitte gebe eine Startuhrzeit an wie z.B 15 Uhr")
        elif(element=='datum'):
            bot.send_message(chat_id,"In deinem Satz ist kein Datum genannt\n Bitte gebe ein Datum an wie z.B 3. Juni/01.01.2021 oder nächsten Mittwoch")

    

def intendCheck(chat_id,ppDict):
    if(ppDict['intend']==None):
        bot.send_message(chat_id,"Ich habe leider keine Absicht in deinem Satz erkannt,bitte schreibe mir was genau du machen möchtest(anzeigen/anlegen/bearbeiten/verschieben/löschen)")

def checkDicForMissingValue(ppDict,intend):
    googleMethoden={'erstellen':['titel','intend','uhrzeit','enduhrzeit','datum'],'zeige an':['datum'],'aendern':['titel','intend','uhrzeit','enduhrzeit','datum'],'loeschen':['uhrzeit','datum'],'verschiebe':['uhrzeit','enduhrzeit','datum']}
    necessaryInput=googleMethoden[intend]
    missingElement=[]
    print(type(missingElement))
    for element in necessaryInput:
        print(element+" for schleife Funkitioniert") 
        if(ppDict[element]==None):
            missingElement.append(element)
        
    return missingElement


    



bot.polling()
