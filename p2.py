import telebot
import datetime
import sqlite3
import schedule
import time
import pytz
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("token")
bot=telebot.TeleBot(token)

bd={}

def obnovlenee_bd():
    conn = sqlite3.connect('time.db')
    cur = conn.cursor()
    sqlite_select_query = """SELECT * from timetable"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    for x in records:
        if x[2] in bd:
            bd[x[2]].add(x[1])
        else:
            bd[x[2]]=set()
            bd[x[2]].add(x[1])
        if x[3] in bd:
            bd[x[3]].add(x[1])
        else:
            bd[x[3]]=set()
            bd[x[3]].add(x[1])

def send_m(a):
    bot.send_message(a,"Попей воды")

def pre_send():
    d=datetime.datetime.now()
    p=d.strftime('%H:%M')

    if p in bd:
        for x in bd[p]:
            send_m(x)

obnovlenee_bd()
schedule.every().minutes.do(pre_send)
schedule.every().minutes.do(obnovlenee_bd)

while True:
    schedule.run_pending()
    time.sleep(1)
