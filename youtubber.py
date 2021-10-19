#!/usr/bin/env python3
# pip3 install youtube-dl

from __future__ import unicode_literals
import youtube_dl
from multiprocessing import Process
import telegram_send

def YTdownload(opts):

    for dlLink in dlLinks:
        with youtube_dl.YoutubeDL(opts) as ydl:

            vidinfo = ydl.extract_info(dlLink, download = True)

            if not ydl.in_download_archive(vidinfo):
                ydl.download([dlLink])
                ydl.record_download_archive(vidinfo)


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        telegram_send.send(messages=[msg])
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

if __name__ == "__main__":

    dlLinks = ['https://www.youtube.com/playlist?list=PLqBeEonnGFpPgfqbHwHcVw-663P6FyC7u']


    HQ_opts = {
        'ignoreerrors': True,
        #'verbose': True,                            # Prints various debugging information
        'download_archive': './#DLHistory',
        'outtmpl': './HQ/'+'%(title)s.%(ext)s',
        'fixup': 'detect_or_warn',
        'format': 'bestaudio/best',
        #'username': 'email',
        #'password': 'password',
        #'writethumbnail': True,
        'addmetadata': True,
        'extractaudio' : True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'best'},
            #{'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'cookiefile': 'cookies.txt'
    }

    YTdownload(HQ_opts)

