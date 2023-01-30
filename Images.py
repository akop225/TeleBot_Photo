import urllib.request
i = 4


def downloader_images(url):
    global i
    urllib.request.urlretrieve(url, f'{i}.mp3')
    i += 1


downloader_images(input())

#  for _ in range(10):
#      downloader_images(input())