
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

    print(pp.__dict__)    
   

    #Bot Antwort vorbereiten
    
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

def botNachfrage(message, typ):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Kein " + typ + " gefunden. Bitte geben Sie die Informationen ein:")
    eingabe = message.text
    return eingabe


bot.polling()