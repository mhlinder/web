#!/usr/bin/env python3

from bs4 import BeautifulSoup
from requests import get

base = 'https://www.youtube.com'
r = get('{}/channel/UCigt36ux93khwf5UzwWhX_A/playlists'.format(base))
soup = BeautifulSoup(r.text)

pl = soup.findAll('a',  {'class': 'yt-ui-ellipsis-2'})
titles = [x.get('title') for x in pl]
urls = ['{0}{1}'.format(base, x.get('href')) for x in pl]

yt_playlists = ''
yt_songlists = ''
for i in range(len(pl)):
    r = get(urls[i])
    soup = BeautifulSoup(r.text)
    songs = soup.findAll('a', {'class': 'yt-uix-tile-link'})

    tmp = '{0}\n<li><a href="{1}">{2}</a></li>'

    yt_playlists = tmp.format(yt_playlists, urls[i], titles[i])

#s = s.substitute(yt_playlists = yt_playlists)

with open('music.html', 'w') as f:
    f.write(yt_playlists)

