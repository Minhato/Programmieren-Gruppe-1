
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
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und verwaltet Ihren Terminkalender\nmit'/help' erhalten Sie eine ausführliche beschreibung aller Funktionalitäten.\nMöge die Organisation deiner Zeit mit dir sein!")
    bot.send_message(chat_id, "Ihr Botler wurde gestartet geben Sie einen Satz ein"+labCoat)


@bot.message_handler(commands=['help'])
def echo_message(message):
    chat_id= message.chat.id
    bot.send_message(chat_id,"Der Botler ist ihr persönlicher Assistent und hilft Ihnen dabei Ordnung in ihre Termine zu bringen"+robot+"\n\nMit dem Botler kannst du Google Calender Termine anlegen,anzeigen,löschen,ändern oder verschieben\n\n""Dazu kannst du einfach einen Satz schreiben, der Botler erledigt den Rest und Fragt zur Not nochmal nach.\n\n\nMit Informationen über Art des Termins,Datum,Uhrzeit und Titel des Termins bist du aber auf der sicheren Seite;)")

#Methoden
def checkAllInputs(userEingabe):
    try:
        pp.titel = getTitel(userEingabe)
    except:
        pp.titel=None
    try:
        pp.intend =getIntend(userEingabe,checkActionKind())
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
    print(intend)
    googleMethoden={'erstellen':['titel','intend','uhrzeit','enduhrzeit','datum'],'zeige an':['datum'],'aendern':['titel','intend','uhrzeit','enduhrzeit','datum'],'loeschen':['uhrzeit','datum'],'verschiebe':['uhrzeit','enduhrzeit','datum']}
    necessaryInput=googleMethoden[intend]
    missingElement=[]
    print(type(missingElement))
    for element in necessaryInput:
        print(element+" for schleife Funkitioniert") 
        if(ppDict[element]==None):
            missingElement.append(element)
        
        
    return missingElement

def checkSpecificInput(userEingabe,chat_id):
    try:
        if pp.titel==None:
            print("Er geht in die Titel schleife rein")
            pp.titel=getTitel(userEingabe)
            if(pp.uhrzeit==None):
                bot.send_message(chat_id,"Kein Titel erkannt,bitte nochmals angeben")
    except:
        print("Except wird aufgerufen")
        bot.send_message(chat_id,"Titel fehlt immernoch")
    try:
        if pp.intend==None:
            pp.intend=getIntend(userEingabe,checkActionKind())
    except:
        bot.send_message(chat_id,"Kein Intend erkannt,bitte erneut angeben")
    try:
        if pp.uhrzeit==None:
            pp.uhrzeit=getUhrzeit(0)
            if(pp.uhrzeit==None):
                bot.send_message(chat_id,"keine StartUhrzeit erkennt,bitte erneut angeben")
    except:
        bot.send_message(chat_id,"keine StartUhrzeit erkennt,bitte erneut angeben")
    try:
        if pp.enduhrzeit==None:
            print("enduhrzeit wird ausgeführt")
            pp.enduhrzeit=getUhrzeit(1)
    except:
        pass
    try:
        if pp.datum==None:
            pp.datum=getDatum(getDateText(userEingabe))
            if(pp.datum==None):
                bot.send_message(chat_id,"Kein Datum gefunden bitte das Datum im dd.dd.dddd Format eingeben")
    except:
        bot.send_message(chat_id,"Kein Datum gefunden bitte das Datum im dd.dd.dddd Format eingeben")

    

#Message Handler
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    #chatID und eingabe erfassen
    chat_id = message.chat.id
    eingabe = message.text
    setText(eingabe)
    global ersteUserNachricht
    print(ersteUserNachricht)
    if (ersteUserNachricht==True):
        checkAllInputs(eingabe)
        if(checkDicForMissingValue(pp.__dict__,pp.intend)==[]):
            formatAndSendMessages(chat_id)
            print(ersteUserNachricht)
            bot.send_message(chat_id, pp.testest())
            ersteUserNachricht=True
        else:
            intendCheck(chat_id,pp.__dict__)
            missingValueArray=checkDicForMissingValue(pp.__dict__,pp.intend)
            ersteUserNachricht =False
            missingValueNachfrage(chat_id,missingValueArray)
            print(pp.__dict__)
            
    else:
        print("2.Else Schelife wurde erreicht")
        checkSpecificInput(eingabe,chat_id)
        print(pp.__dict__)
        if(checkDicForMissingValue(pp.__dict__,pp.intend)==[]):
            formatAndSendMessages(chat_id)
            bot.send_message(chat_id, pp.testest())
            ersteUserNachricht=True

        


        
        




    

    #pp.ausgeben()
    #pp.testest()
    #Bot Antwort vorbereiten
    #intendCheck(chat_id,pp.__dict__)






bot.polling()
