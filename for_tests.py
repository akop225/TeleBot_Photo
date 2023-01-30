import vk_api
from vk_api.audio import VkAudio


def main():
    vk_session = vk_api.VkApi('89854218373', 'Akop2003')

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        # Если происходит исключение во время аутентификации, то выводим ошибку и выходи
        print(error_msg)
        return

    # Модуль для получения аудиозаписей без использования официального API.
    vkaudio = VkAudio(vk_session)

    for track in vkaudio.get_iter():
        f = open('TAKE.mp3', 'wb')
        f = track
        print(track)
        print(f"Исполнитель : {track.get('artist')}")
        print(f"Название трека : {track.get('title')}")
        print(f"Ссылка на трек(url) : {track.get('url')}")
        print('--------------------------------------------')


if __name__ == '__main__':
    main()
