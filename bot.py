import telebot
from configparser import ConfigParser
from telebot import types as t
import dadosapi
import database

config = ConfigParser()
config.read('bot.conf')

TOKEN = config['BRCORONAVIRUSBOT']['TEST_TOKEN']

bot = telebot.TeleBot(TOKEN)

botoes = t.ReplyKeyboardMarkup()
botao1 = t.KeyboardButton('Dados recentes')
botoes.add(botao1)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Aperte o botão <b>Dados recentes</b> para obter o balanço mais recente'
                          ' de Coronavírus no Brasil.\n\n'
                          'Clique em /cadastrar para receber notificações dos dados atualizados por dia.',
                     reply_markup=botoes,
                     parse_mode='HTML')


@bot.message_handler(commands=['cadastrar'])
def register(msg):
    chatid = msg.chat.id
    userid = msg.from_user.id
    if database.register(chatid, userid):
        bot.send_message(chat_id=msg.chat.id, text='Usuário cadastrado com sucesso!')
    else:
        bot.send_message(chat_id=msg.chat.id, text='Usuário já está cadastrado.')


@bot.message_handler(func=lambda m: m.text == 'Dados recentes')
def send_recent_cases(msg):
    titulo = '\U0001F7E1 <b>Dados recentes de Covid-19 no Brasil</b>\n\n'
    cases = dadosapi.brazil_recent_cases()
    texto = titulo + cases
    bot.send_message(chat_id=msg.chat.id, text=texto, reply_markup=botoes, parse_mode='HTML')


bot.polling(timeout=20, none_stop=True)
