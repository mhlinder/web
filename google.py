
db_path = 'ServerDatabase.db'

from gmusicapi import Mobileclient
from re import compile
from sqlite3 import connect

# Establish a connection to a local Google Play MusicManager sqlite
# database, with local file paths for any songs that I uploaded to Google Play
conn = connect(db_path)
c = conn.cursor()

# The first line of secret_google.txt is the Google Music user email,
# the second line the user password
with open('secret_google.txt') as f:
    r = [l.strip() for l in f.readlines()]

api = Mobileclient()
api.login(r[0], r[1], Mobileclient.FROM_MAC_ADDRESS)

playlists = api.get_all_user_playlist_contents()

# All playlists to record start with a four digit integer
format_check = compile('^[0-9]{3}')

for playlist in playlists:
    if format_check.search(playlist['name']) is not None:
        for t in playlist['tracks']:
            if t['source'] == '1':
                print('This file was uploaded')
                tt = t
            else:
                track = t['track']
                print('This file is hosted by Google')
                print("'{0}' by {1}".format(track['title'], track['artist']))
            print('---')

# c.execute('SELECT * FROM XFILES')

