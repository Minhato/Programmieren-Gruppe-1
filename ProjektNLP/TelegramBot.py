
#from NLP_Calendar.Logik import Logik
import telebot
import spacy
from  Logik import *
from telebot import types

ersteUserNachricht=True
#TheBotler
tokenAPI = '1816801935:AAHAH98soREBBJvN2MQOAT4FaaCByDevG9w'
pp = Logik()
#Emojii register
labCoat = u'\U0001F97C' 
robot= u'\U0001F916'

bot = telebot.TeleBot(tokenAPI)
@bot.message_handler(commands=['start'])
def echo_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und verwaltet Ihren Terminkalender\nmit'/help' erhalten Sie eine ausführliche beschreibung aller Funktionalitäten.\nMöge die Organisation deiner Zeit mit dir sein!")
    bot.send_message(chat_id, "Ihr Botler wurde gestartet geben Sie einen Satz ein"+labCoat)
    
    
    print("stratet")
@bot.message_handler(commands=['help'])
def echo_message(message):
    chat_id= message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und hilft Ihnen dabei Ordnung in ihre Termine zu bringen"+robot+"\n\nMit dem Botler kannst du Google Calender Termine anlegen,anzeigen,löschen,ändern oder verschieben\n\n""Dazu kannst du einfach einen Satz schreiben, der Botler erledigt den Rest und Fragt zur Not nochmal nach.\n\n\nMit Informationen über Art des Termins,Datum,Uhrzeit und Titel des Termins bist du aber auf der sicheren Seite;)")

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
        print(type(pp.datum))
        print(pp.datum)
        #pp.datum = datetime.strptime(pp.datum, "%d" "." "%m" "." "%Y").date()
        print(type(pp.datum))
    except: 
        pp.datum=None
    
    print("das dict:") 
    print(pp.__dict__)

    #pp.datum = datetime(2021,6,10)
    pp.ausgeben()
    pp.testest()
    
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
    try:
        bot.send_message(chat_id,missingValueNachfrage(chat_id,checkDicForMissingValue(pp.__dict__,pp.intend)))
    except:
        bot.send_message(chat_id, chatTitel)
        bot.send_message(chat_id, chatUhrzeit)
        bot.send_message(chat_id, chatEndUhrzeit)
        bot.send_message(chat_id, chatIntend)
        bot.send_message(chat_id, chatDatum)


#Methoden
def missingValueNachfrage(chat_id, missingValues):
    for element in missingValues:
        if(element=='titel'):
            bot.send_message(chat_id,"Ich konnte aus deinem Satz leider keinen Titel erkennen\nBitte gebe einen Titel an wie z.B Skaten mit Minh")
        elif(element=='uhrzeit'):
            bot.send_message(chat_id,"In deinem Satz ist keine Anfangsuhrzeit des Termines angegeben\nBitte gebe eine Startuhrzeit an wie z.B 15 Uhr")
        elif(element=='datum'):
            bot.send_message(chat_id,"In deinem Satz ist kein Datum genannt\n Bitte gebe ein Datum an wie z.B 3. Juni/01.01.2021 oder nächsten Mittwoch")


def intendCheck(chat_id,ppDict):
    if(ppDict['intend']==None):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Anzeigen')
        itembtn2 = types.KeyboardButton('Erstellen')
        itembtn3 = types.KeyboardButton('Bearbeiten')
        itembtn4 = types.KeyboardButton('Verschieben')
        itembtn5 = types.KeyboardButton('Loeschen')
        markup.add(itembtn1, itembtn2, itembtn3,itembtn4,itembtn5)
        bot.send_message(chat_id, "Wähle einen Intent aus:", reply_markup=markup)     

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
