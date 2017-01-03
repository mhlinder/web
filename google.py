
# Formatting string
title_by_artist = "'{0}' by {1}"

db_path = 'ServerDatabase.db'
# Columns in the table XFILES
schema = ['Id', 'RootId', 'FileHandle', 'RevisionAdded',
          'RevisionDeleted', 'FieldUpdateRevision', 'DisplayName',
          'DisplayPath', 'IsFolder', 'Size', 'FileType', 'Usage',
          'DateCreated', 'DateModified', 'TranscodingType',
          'MusicChannels', 'MusicName', 'MusicAlbum', 'MusicArtist',
          'MusicAlbumArtist', 'MusicComposer', 'MusicComment',
          'MusicGenre', 'MusicYear', 'MusicDuration',
          'MusicTrackCount', 'MusicTrackNumber', 'MusicDiscCount',
          'MusicDiscNumber', 'MusicCompilation', 'MusicBitRate',
          'MusicSampleRate', 'MusicBpm', 'MusicAlbumArtStart',
          'MusicAlbumArtSize', 'MusicAlbumArtType', 'MusicAlbumArt',
          'MusicStart', 'MusicLength', 'MD5Hash', 'ServerId',
          'MusicRating', 'MusicPlayCount', 'MusicDateAdded',
          'MusicDatePlayed', 'MusicUploadStatus',
          'MusicUploadSelected', 'MusicLastScanned', 'MusicIsPodcast',
          'StoreType', 'MusicLabelCode', 'MusicUitsJson',
          'MusicContentRating', 'MusicAdditionalMetadataJson',
          'DeleteAfterUpload', 'RowLastModified',
          'MusicUploadStatusLastModified'] 

from gmusicapi import Mobileclient
from re import compile
from sqlite3 import connect

# Establish a connection to a local Google Play MusicManager sqlite
# database, with local file paths for any songs that I uploaded to Google Play
conn = connect(db_path)
c = conn.cursor()

# The first line of secret_google.txt is a Google Music user email,
# the second line the user's password
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
                ## 'trackId' corresponds to column 'ServerId' in table XFILES
                selector = "SELECT * FROM XFILES WHERE ServerId='{}'" 
                c.execute(selector.format(t['trackId']))
                matches = c.fetchall()
                if len(matches) == 1:
                    m = matches[0]
                    lookup = dict(zip(schema, m))
                    print(title_by_artist.format(lookup['MusicName'],
                                                 lookup['MusicArtist']))
                else:
                    print('Weirdness in playlist {}'.format(playlist['name']))
                    
            else:
                track = t['track']
                print(title_by_artist.format(track['title'], track['artist']))

