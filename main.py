import telebot
from config import TOKEN, exchanger
from extensions import Converter, ConverterException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(messege: telebot.types.Message):
    text = r'''/values - список предлогаемых к переводу валют ,
Валюта №1 Валюта №2 Сумма - производится перевод суммы из Валюты №1 в Валюту №2'''
    bot.send_message(messege.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные к переводу валюты:\n'
    text += "\n".join(f"{i+1}) {key}" for i, key in enumerate(exchanger.keys()))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Converter.get_price(values)
    except ConverterException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {values[0]} {values[1]} в {values[2]} -- {result} {exchanger[values[1]]}'
        bot.reply_to(message, text)


bot.polling(none_stop=True, interval=0)