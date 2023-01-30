import time
import sqlite3
import vk_api
from vk_api import audio
import requests
from time import time
import os


REQUEST_STATUS_CODE = 200
name_dir = 'music_vk'
login = '89854218373'  # Номер телефона
password = 'Akop2003'  # Пароль
my_id = 'jaaacob'  # Ваш id vk

if not os.path.exists(name_dir):
    os.makedirs(name_dir)


vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth()
vk = vk_session.get_api()  # Теперь можно обращаться к методам API как к обычным
                                        # классам
vk_audio = audio.VkAudio(vk_session)  # Получаем доступ к audio

os.chdir(name_dir)

time_start = time()
for i in vk_audio.get():
    print(i)
    try:
        r = requests.get(i["url"])
        if r.status_code == REQUEST_STATUS_CODE:
            with open(i["artist"] + '_' + i["title"] + '.mp3', 'wb') as output_file:
                output_file.write(r.content)
    except OSError:
        print(i["artist"] + '_' + i["title"])
time_finish = time()
print("Time seconds:", time_finish - time_start)