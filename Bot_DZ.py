import telebot
from config import TOKEN,slovar
from extensions import APIException,ConverterPrice


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start',])
def send_welcome(message):
    text = f'Я вас приветствую {message.chat.first_name}{message.chat.last_name}.Чтобы узнать как записывать данные в конвектор валют воспользуйтесь командой /help'
    bot.reply_to(message,text)

@bot.message_handler(commands=['help'])
def help(message):
    text = 'Введите в таком порядке <название валюты> пробел <в какую валюту хотите перевести> пробел <количество> отправить. Название доступных валют вы узнаете воспользовавшись коммандой /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\nдоллар\nевро\nбиткоин\nрубль'
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convektor(message:telebot.types.Message):
    text_uzer = message.text.split(' ')
    try:
        if len(text_uzer) != 3:
            raise APIException('Количество параметров не совпадает с требованиями')

        quote,base,amount = text_uzer

        a = ConverterPrice.get_price(quote,base,amount)

        otvet = a * int(amount)
    except APIException as e:
        bot.reply_to(message,f'Ошибка пользователя {e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду  {e}')
    else:
        bot.send_message(message.chat.id,f'Цена {amount} {quote} в {base} = {otvet}')

bot.polling(none_stop=True)