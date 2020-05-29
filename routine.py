import telebot
import configparser
import database
import dadosapi

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bot.conf')

    TOKEN = config['BRCORONAVIRUSBOT']['TEST_TOKEN']

    bot = telebot.TeleBot(TOKEN)

    chatid_list = database.notify()
    for chatid in chatid_list:
        titulo = '\U0001F6A8 <b>Dados recentes de Covid-19 no Brasil</b>\n\n'
        cases = dadosapi.brazil_recent_cases()
        texto = titulo + cases
        bot.send_message(chat_id=chatid, text=texto, parse_mode='HTML')
