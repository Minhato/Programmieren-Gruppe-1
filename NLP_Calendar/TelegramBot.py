import telebot
import spacy

#TheBotler
tokenAPI = '1816801935:AAHAH98soREBBJvN2MQOAT4FaaCByDevG9w'

bot = telebot.TeleBot(tokenAPI)
@bot.message_handler(commands=['start'])
def echo_message(message):
    chat_id = message.chat.id    
    bot.send_message(chat_id, "Der beste Botler")
    print("stratet")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    chat_id = message.chat.id
    eingabe = message.text
    result = "yeet"
    bot.send_message(chat_id, result)
    print("Test")

bot.polling()