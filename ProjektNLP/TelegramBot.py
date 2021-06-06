
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
    pp.titel = getTitel(eingabe) 
    pp.intend =getIntend(eingabe,checkActionKind())
    pp.uhrzeit = getUhrzeit(0)
    pp.enduhrzeit = getUhrzeit(1)
    pp.datum=getDatum(getDateText(eingabe))
   

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

bot.polling()