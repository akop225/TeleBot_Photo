import sqlite3
NAME_OF_DATA = 'telebot_data.db'

def start_price_and_size(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT price FROM SizesAndPrices WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    if not lst:
        req = f"""INSERT INTO SizesAndPrices VALUES({chat_id}, 36, 45, 5000);"""
        cur.execute(req)
        con.commit()


def get_price(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT price FROM SizesAndPrices WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    con.commit()
    price = lst[0]
    return price

def update_price(chat_id, new_price):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""UPDATE SizesAndPrices SET price = {new_price} WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    con.commit()

def get_min_size(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT min_size FROM SizesAndPrices WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    con.commit()
    min_size = lst[0]
    return min_size

def update_min_size(chat_id, new_size):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""UPDATE SizesAndPrices SET min_size = {new_size} WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    con.commit()

def get_max_size(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT max_size FROM SizesAndPrices WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    con.commit()
    max_size = lst[0]
    return max_size

def update_max_size(chat_id, new_size):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""UPDATE SizesAndPrices SET max_size = {new_size} WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    con.commit()