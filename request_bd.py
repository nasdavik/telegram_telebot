import pymysql
from config import host, user, password, db_name


def connect():
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
# функция для соедениения


def writing(date, content):
    connection = connect()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO calendar (date, result) VALUES('{date}','{content}');")
                connection.commit()
    except Exception as ex:
        pass


def updating(date, content):
    connection = connect()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE calendar SET result = '{content}' WHERE date = '{date}';")
                connection.commit()
    except Exception as ex:
        pass


def info_day(date):
    connection = connect()
    info = []
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(date,'%d.%m.%Y') AS date, result FROM calendar WHERE date = '{date}';")
            data = cursor.fetchall()
            for item in data:
                info.append(item)
            return info[0]["result"]
    except Exception as ex:
        pass


def info_month(month, year):
    connection = connect()
    info = []
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT DATE_FORMAT(date,'%d') AS date, result FROM calendar WHERE MONTH(date) = {month} AND YEAR(date) = {year};")
            data = cursor.fetchall()
            for item in data:
                info.append(item)
            return [list(x.values()) for x in info]
    except Exception as ex:
        pass


def info_calender():
    connection = connect()
    info = []
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT result FROM calendar ORDER BY date DESC;")
            data = cursor.fetchall()
            for item in data:
                info.append(item)
            ans = 0
            for x in info:
                if x["result"] == "отлично":
                    ans += 1
                else:
                    break
            return ans
    except Exception as ex:
        pass


def check_date(date):
    connection = connect()
    info = []
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT result FROM calendar WHERE date = '{date}';")
            data = cursor.fetchall()
            info.extend([x for x in data])
            return info[0]["result"]
    except Exception as ex:
        pass


def info_balance():
    connection = connect()
    info = []
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM balance;")
            data = cursor.fetchall()
            for item in data:
                info.append(item)
            return info[0]['my_balance']
    except Exception as ex:
        pass


def upd_balance(value):
    connection = connect()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE balance SET my_balance = '{value}'")
                connection.commit()
    except Exception as ex:
        pass

