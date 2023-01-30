import sqlite3
NAME_OF_DATA = 'telebot_data.db'

def get_state(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT numb_of_state FROM states WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    state = lst[0] if lst else 0
    if not lst:
        req = f"""INSERT INTO states VALUES({chat_id}, 0, 35);"""
        cur.execute(req)
        con.commit()
    return state


def update_state(chat_id, state):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""UPDATE states SET numb_of_state = {state} WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    con.commit()


def get_percent_of_sight(chat_id):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""SELECT percent_of_sight FROM states WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    lst = cur.fetchone()
    con.commit()
    percent_of_sight = lst[0]
    return percent_of_sight


def update_percent_of_sight(chat_id, percent_of_sight):
    con = sqlite3.connect(NAME_OF_DATA)
    cur = con.cursor()
    req = f"""UPDATE states SET percent_of_sight = {percent_of_sight} WHERE chat_id LIKE {chat_id};"""
    cur.execute(req)
    con.commit()