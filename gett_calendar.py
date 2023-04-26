from request_bd import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def my_calendar(month, year):
    month_of_the_year = {"январь": "01", "февраль": "02",
                         "март": "03", "апрель": "04", "май": "05",
                         "июнь": "06", "июль": "07", "август": "08",
                         "сентябрь": "09", "октябрь": "10",
                         "ноябрь": "11", "декабрь": "12"}

    back = np.zeros([1200, 1200, 4], dtype=np.uint8)
    back[::] = [0, 0, 0, 150]
    img2 = Image.fromarray(back)
    #создаю изображение для затемнения фона

    img = Image.open(f'photo/{month_of_the_year[month]}.jpg')
    img.paste(img2, (0,0), img2)
    #открываю нужное фото и накладываю фон

    img_draw = ImageDraw.Draw(img)
    y = 300
    for i in range(7):
        img_draw.line((0, y, 1200, y), width=4)
        y += 150
    x = 0
    for i in range(7):
        img_draw.line((x, 300, x, 1200), width=4)
        x += 200
    font = ImageFont.truetype("font/font_for_text.ttf", size=130)
    img_draw.text((600, 170), month, font=font, fill='white', anchor="mm")
    # рисую сетку для дат и пишу название месяца

    data = info_month(month_of_the_year[month], year)
    # выбираю подходящие даты по году и месяцу

    result_day = []
    date_day = []
    for dat in data:
        result_day.append(dat[1])
        date_day.append(dat[0])
    how_good = iter(result_day)
    day = iter(date_day)
    mood = {"отлично": "#00ff1e", "неплохо": "yellow", "плохо": "red"}
    # получаю итератор с результатами, итератор из дат и словарь для цветов

    for y in range(375, 1200, 150):
        for x in range(100, 1200, 200):
            try:
                img_draw.text((x, y), next(day), font=font, fill=mood[next(how_good)], anchor="mm")
            except:
                break
    # записываю все необходимое на картинку

    return img
