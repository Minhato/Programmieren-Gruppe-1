
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
    bot.send_message(chat_id, "Ihr Botler wurde gestartet geben Sie einen Satz ein")
    print("stratet")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    chat_id = message.chat.id
    eingabe = message.text
    print("eingabetyp:",type(eingabe))
    #p1.titel = getTitel(str(eingabe))
    pp.titel = getTitel(eingabe)
    print("p1 titel",pp.titel)
    print(type(pp.titel))
    pp.titel = str(pp.titel)
    print(type(pp.titel))
    print(eingabe)
    #result = p1.titel
    pp.uhrzeit = getUhrzeit()[0]
    result = "Titel lautet: " + str(pp.titel)
    print("result ",type(result), result)
    bot.send_message(chat_id, result)
    uhrzeit = "Anfangsuhrzeit ist: " + str(pp.uhrzeit) + " Uhr"
    bot.send_message(chat_id, uhrzeit)
    print("Test")

bot.polling()