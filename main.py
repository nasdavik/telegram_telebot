import telebot
from telebot import types
from auth_data import token
import json
import re
from gett_calendar import my_calendar


bot = telebot.TeleBot(token)


class MyBalance:
    def __init__(self):
        with open("balance.txt") as reader:
            for r in reader:
                self.balance = int(r)
        with open("BD.json", encoding="utf-8") as reaeder:
            data = json.load(reaeder)
            self.days = 0
            for i in data.values():
                if i == 'отлично': self.days += 1
                elif i == 'неплохо': self.days = self.days//2
                elif i == 'плохо': self.days = 0

    def rewriting(self):
        with open("BD.json", encoding="utf-8") as reaeder:
            data = json.load(reaeder)
            self.days = 0
            for i in data.values():
                if i == 'отлично': self.days += 1
                elif i == 'неплохо': self.days = self.days//2
                elif i == 'плохо': self.days = 0

    def gett_days(self):
        return self.days

    def gett_balance(self):
        return self.balance

    def plus(self):
        if self.days == 365: self.balance += 3000
        elif self.days == 180: self.balance += 1000
        elif self.days == 90: self.balance += 500
        elif self.days == 30: self.balance += 300
        elif self.days == 14: self.balance += 100
        elif self.days == 7: self.balance += 50
        with open("balance.txt", "w", encoding="utf-8") as writer: writer.write(str(self.gett_balance()))

    def minus(self, x):
        self.balance = self.balance - x
        with open("balance.txt", "w", encoding="utf-8") as writer: writer.write(str(self.gett_balance()))


katya = MyBalance()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет, я пострался сделать полезного бота для тебя. Хоть это и моя первая программа, надеюсь со своей задачей она справится. Все что может тебе пригодится я постарался расписать в /help")


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    write_down = types.KeyboardButton("Записать день 📝")
    balance = types.KeyboardButton("Баланс 💵")
    rewriter = types.KeyboardButton("Изменить день 📅")
    helping = types.KeyboardButton("Помощь 🛑")
    markup.add(write_down, rewriter, balance, helping)
    bot.send_message(message.chat.id, "Если ты хочешь посмотреть отчет за прошлые дни, то ты можешь:\n"
                                      "- Написать в формате: Отчет 20.05.2019, для получения результата о конкретном дне\n"
                                      "- Написать в формате: Календарь Май 2019, для получения результата о конкретном меcяце в году\n\n"
                                      "Ну и кнопочками еще пользуйся",
                                        reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "записать день 📝":
        bot.send_message(message.chat.id,
                         "Нужно написать дату в формате - (день.месяц.год). И написать итог дня (Отлично, Неплохо, Плохо). Пример: 20.05.2019 Отлично")

    elif re.match(r"\d\d\.\d\d\.\d{4}", message.text.lower()):
        w = message.text.lower().split()
        try:
            t = {w[0]:w[1]}
        except:
            bot.send_message(message.chat.id,
                             "Похоже вы написали только дату. Стоит поробывать еще раз 🙂")
        else:
            if w[1]=="отлично" or w[1]=="неплохо" or w[1]=="плохо":
                with open("BD.json", encoding="utf-8") as reader:
                    data = json.load(reader)
                    if w[0] not in data:
                        data[w[0]] = w[1]
                        with open("BD.json", "w", encoding="utf-8") as writer:
                            json.dump(data, writer, ensure_ascii=False, indent=4)
                        bot.send_message(message.chat.id,
                                         "Отлично, я все записал")
                        if w[1] == 'отлично': katya.days += 1
                        elif w[1] == 'неплохо': katya.days = katya.days//2
                        elif w[1] == 'плохо': katya.days = 0
                        katya.plus()
                    else:
                        bot.send_message(message.chat.id,
                                         "Хммм... 🤔\nПохоже у меня есть об этом информация. Стоит проверить сообщение и поробывать еще раз 👀")
            else:
                bot.send_message(message.chat.id, "В резултатах дня нужно указать:\n"
                                                  "- Отлично, в случае если вредности вообще не поедались ✅\n"
                                                  "- Неплохо, в случае если немного вредностей было ⚠️\n"
                                                  "- Плохо, в случае если вредности были ⛔")

    elif re.match("изменить день 📅", message.text.lower()):
        bot.send_message(message.chat.id, "Для того что-бы отредактировать результат интересующего "
                                          "дня, нужно написть запрос по типу - \"Перезаписать 02.07.2002 Отлично\". "
                                          "Просто пишешь дату и на что изменить")

    elif re.match(r"перезаписать \d\d\.\d\d\.\d{4} .*", message.text.lower()):
        rewrite = message.text.lower().split()
        with open("BD.json", encoding="utf-8") as for_rew:
            data_rew = json.load(for_rew)
        if rewrite[1] in data_rew:
            data_rew[rewrite[1]] = rewrite[2]
            with open("BD.json", "w", encoding="utf-8") as fr:
                json.dump(data_rew, fr, ensure_ascii=False, indent=4)
                bot.send_message(message.chat.id, "Все готово!")
            katya.rewriting()
            katya.plus()
        else:
            bot.send_message(message.chat.id,
                             "Упс, ошибочка. что-то не так в твоем сообщениии. Этот день точно у тебя записан?")


    elif re.match("календарь", message.text.lower()):
        text = message.text.lower().split()
        try:
            bot.send_photo(message.chat.id, my_calendar(text[1], text[2]))
        except:
            bot.send_message(message.chat.id, "Похоже у меня нет об этом информации. Возможно в твоем сообщении ошибка")

    elif re.search(r"отч[её]т \d\d.\d\d.\d{4}", message.text.lower()):
        with open("BD.json", encoding="utf-8") as reader_2:
            mess = message.text.lower().split()
            date = json.load(reader_2)
            if mess[1] in date:
                if date[mess[1]] == "отлично":
                    bot.send_message(message.chat.id, "В этот  день твой результат:\nОтлично 🟢")
                elif date[mess[1]] == "неплохо":
                    bot.send_message(message.chat.id, "В этот  день твой результат:\nНеплохо 🟡")
                elif date[mess[1]] == "плохо":
                     bot.send_message(message.chat.id, "В этот  день твой результат:\nПлохо 🔴")
                else:
                    bot.send_message(message.chat.id, "Похоже какая-то ошибка связана я этим днем. Нужно сказать об этом Дане")
            else:
                bot.send_message(message.chat.id, "К сожалению у меня нет информации об этом дне😾")

    elif message.text.lower() == "баланс 💵":
        bot.send_message(message.chat.id, f"Твой баланс: {katya.gett_balance()}р.")

    elif re.match("списать", message.text.lower()):
        m = message.text.lower().split()
        if len(m) > 1:
            try:
                katya.minus(int(m[1]))
                bot.send_message(message.chat.id, f"Успешно! Твой баланс: {katya.gett_balance()}р.")
            except:
                bot.send_message(message.chat.id, "Вычетание не работает коректно")
        else:
            bot.send_message(message.chat.id, "В твоем сообщении допущена ошибка. Ты не указал сумму")

    elif re.match("помощь 🛑", message.text.lower()):
        help_message(message)

    else:
        bot.send_message(message.chat.id, "Не совсем понял что ты хочешь. У тебя есть кнопка Помощь 🛑 (/help),  воспользуйся ей или другими кнопками")


bot.polling(none_stop=True)