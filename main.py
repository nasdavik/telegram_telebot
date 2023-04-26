import telebot
from telebot import types
from auth_data import token
import re
import time
from gett_calendar import my_calendar
from request_bd import *

bot = telebot.TeleBot(token)


class MyBalance:
    def __init__(self):
        self.balance = info_balance()
        self.days = info_calender()

    def upd_days(self):
        self.days = info_calender()

    def gett_balance(self):
        return self.balance

    def plus(self):
        if self.days == 365:
            self.balance += 9300
        elif self.days == 180:
            self.balance += 3100
        elif self.days == 90:
            self.balance += 1100
        elif self.days == 30:
            self.balance += 270
        elif self.days == 14:
            self.balance += 110
        elif self.days == 7:
            self.balance += 50
        upd_balance(self.balance)

    def minus(self, x):
       self.balance -= x
       upd_balance(self.balance)


katya = MyBalance()


def convert(value):
    return "-".join(value.split(".")[::-1])
# переводит дату в нужный формат для БД

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
write_down = types.KeyboardButton("Записать день 📝")
balance = types.KeyboardButton("Баланс 💵")
rewriter = types.KeyboardButton("Изменить день 📅")
helping = types.KeyboardButton("Помощь 🛑")
markup.add(write_down, rewriter, balance, helping)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет, я пострался сделать полезного бота для тебя. Хоть это и моя первая программа, надеюсь со своей задачей она справится. Все что может тебе пригодится я постарался расписать в /help",
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Если ты хочешь посмотреть отчет за прошлые дни, то ты можешь:\n"
                                      "- Написать в формате: Отчет 20.05.2019, для получения результата о конкретном дне\n"
                                      "- Написать в формате: Календарь Май 2019, для получения результата о конкретном меcяце в году\n\n"
                                      "Ну и кнопочками еще пользуйся",
                                        reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "записать день 📝":
        bot.send_message(message.chat.id,
                         "Нужно написать дату в формате - (день.месяц.год). И написать итог дня (Отлично, Неплохо, Плохо). Пример: 20.05.2019 Отлично", reply_markup=markup)

    elif re.match(r"\d\d\.\d\d\.\d{4}", message.text.lower()):
        w = message.text.lower().split()
        try:
            t = {w[0]:w[1]}
        except:
            bot.send_message(message.chat.id,
                             "Похоже вы написали только дату. Стоит попробывать еще раз 🙂",
                             reply_markup=markup)
        else:
            if w[1] in ("отлично", "неплохо", "плохо"):
                if not check_date(convert(w[0])):
                    try:
                        writing(convert(w[0]), w[1])
                        katya.upd_days()
                        katya.plus()
                        bot.send_message(message.chat.id,
                                         "Отлично, я все записал",
                                         reply_markup=markup)

                    except:
                        bot.send_message(message.chat.id,
                                         "Что-то не так, не удалось записать :(",
                                         reply_markup=markup)
                else:
                    bot.send_message(message.chat.id,
                                     "Хммм... 🤔\nПохоже у меня есть об этом информация. Стоит проверить сообщение и попробывать еще раз 👀",
                                     reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "В резултатах дня нужно указать:\n"
                                                  "- Отлично, в случае если вредности вообще не поедались ✅\n"
                                                  "- Неплохо, в случае если немного вредностей было ⚠️\n"
                                                  "- Плохо, в случае если вредности были ⛔",
                                 reply_markup=markup)

    elif re.match("изменить день 📅", message.text.lower()):
        bot.send_message(message.chat.id, "Для того что-бы отредактировать результат интересующего "
                                          "дня, нужно написть запрос по типу - \"Перезаписать 02.07.2002 Отлично\". "
                                          "Просто пишешь дату и на что изменить",
                         reply_markup=markup)

    elif re.match(r"перезаписать \d\d\.\d\d\.\d{4} .*", message.text.lower()):
        rewrite = message.text.lower().split()
        if check_date(convert(rewrite[1])):
            try:
                if rewrite[2] in ("отлично", "неплохо", "плохо"):
                    updating(convert(rewrite[1]), rewrite[2])
                    katya.upd_days()
                    katya.plus()
                    bot.send_message(message.chat.id, "Все готово!",
                                     reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Ты ведь знаешь, что такое записать нельзя. Можно только отлично, непллохо или плохо",
                                     reply_markup=markup)
            except:
                bot.send_message(message.chat.id, "Ошибка при обновлениии данных. Что конкретно не так - не понятно, нужно ковырять код",
                                 reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             "Упс, ошибочка. что-то не так в твоем сообщениии. Этот день точно у тебя записан?",
                             reply_markup=markup)

    elif re.match("календарь", message.text.lower()):
        text = message.text.lower().split()
        try:
            bot.send_photo(message.chat.id, my_calendar(text[1], text[2]),
                           reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "Похоже у меня нет об этом информации. Возможно в твоем сообщении ошибка",
                             reply_markup=markup)

    elif re.search(r"отч[её]т \d\d.\d\d.\d{4}", message.text.lower()):
        mess = message.text.lower().split()
        if check_date(convert(mess[1])):
            if info_day(convert(mess[1])) == "отлично":
                bot.send_message(message.chat.id, "В этот  день твой результат:\nОтлично 🟢",
                                 reply_markup=markup)
            elif info_day(convert(mess[1])) == "неплохо":
                bot.send_message(message.chat.id, "В этот  день твой результат:\nНеплохо 🟡",
                                 reply_markup=markup)
            elif info_day(convert(mess[1])) == "плохо":
                bot.send_message(message.chat.id, "В этот  день твой результат:\nПлохо 🔴",
                                 reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Похоже какая-то ошибка связана я этим днем. Нужно сказать об этом Дане",
                                 reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "К сожалению у меня нет информации об этом дне😾",
                             reply_markup=markup)

    elif message.text.lower() == "баланс 💵":
        bot.send_message(message.chat.id, f"Твой баланс: {katya.gett_balance()}р.",
                         reply_markup=markup)

    elif re.match("списать", message.text.lower()):
        m = message.text.lower().split()
        if len(m) > 1:
            try:
                katya.minus(int(m[1]))
                bot.send_message(message.chat.id, f"Успешно! Твой баланс: {katya.gett_balance()}р.",
                                 reply_markup=markup)
            except:
                bot.send_message(message.chat.id, "Вычетание не работает коректно",
                                 reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "В твоем сообщении допущена ошибка. Ты не указал сумму",
                             reply_markup=markup)

    elif re.match("помощь 🛑", message.text.lower()):
        help_message(message)

    else:
        bot.send_message(message.chat.id, "Не совсем понял что ты хочешь. У тебя есть кнопка Помощь 🛑 (/help),  воспользуйся ей или другими кнопками",
                         reply_markup=markup)


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(8)
