#!/usr/bin/env python3

# updated 6 january 2019 using
# * python==3.7.2rc1
# * gmusicapi==11.1.1

outfile = 'itunes.html'
rootdir = '/Users/henry/Dropbox/Programming/active/web'

from string import ascii_letters, digits
import re
import sqlite3

from gmusicapi import Mobileclient

alphanum = ascii_letters + digits + '-'
## Display format -- 'Song' by So and so
title_by_artist = "'{0}' - {1}"

def add_to_out(out, s):
    return('{0}{1}'.format(out, s))

def get_google(db_path = 'ServerDatabase.db'):
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
    
    # Establish a connection to a local Google Play MusicManager sqlite
    # database, with local file paths for any songs that I uploaded to Google Play
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # The first line of secret_google.txt is a Google Music user email,
    # the second line the user's password
    with open('secret_google.txt') as f:
        r = [l.strip() for l in f.readlines()]
    
    api = Mobileclient()
    # api.login(r[0], r[1], Mobileclient.FROM_MAC_ADDRESS)
    api.login(r[0], r[1], 'ios:585C130D-12A8-4AAD-847A-A04A64B44A9A')
    
    # All playlists to record start with a three digit integer
    format_check = re.compile('^[0-9]{3}(?::|$)')
    # Note the clash between the search string ':' and the syntax of
    # non-capturing groups in regexes (?:...)
    
    inplaylists = api.get_all_user_playlist_contents()
    playlists = [p for p in inplaylists if format_check.search(p['name']) is not None]
    playlists = sorted(playlists, key = lambda k: k['name'])
    playlists = playlists[1:] + playlists[:1]
    
    google = '2017-01--'

    keys = list()
    keys.append(google)
    
    out = '''
    
    
    <li><div id="{0}">
      <strong><a href="#" id="{0}-title">{1}</a></strong>
      <div id="{0}-body" style="display: none;">\n<ul class="space-before space-after">'''.format(google, google.replace('--', '&ndash;'))
    
    for playlist in playlists:
        pn = playlist['name']

        entries = list()
        for t in playlist['tracks']:
            if t['source'] == '1':
                ## 'trackId' corresponds to column 'ServerId' in table XFILES
                selector = "SELECT * FROM XFILES WHERE ServerId='{}'"
                c.execute(selector.format(t['trackId']))
                matches = c.fetchall()
                if len(matches) == 1:
                    m = matches[0]
                    lookup = dict(zip(schema, m))
                    s = title_by_artist.format(lookup['MusicName'], lookup['MusicArtist'])
                    entries.append('<li>{0}</li>'.format(s))
                else:
                    print('Weirdness in playlist {}. Track info:'.format(playlist['name']))
                    print(t)

            else:
                track = t['track']
                s = title_by_artist.format(track['title'], track['artist'])
                entries.append('<li>{0}</li>'.format(s))
        p_txt   = '\n'.join(entries)
        p_title = ''.join([c for c in pn.replace(' ', '-') if c in alphanum])
        keys.append(p_title)
        out = add_to_out(out, '''

    <li><div id="{1}">
      <a href="#" id="{1}-title">{0}</a>

      <div id="{1}-body" style="display: none;">
    <ol class="space-before space-after">
      {2}
    </ol>
  </div> <!-- #{1}-body -->
</div> <!-- #{1} -->
</li>'''.format(pn, p_title, p_txt))

    out = add_to_out(out, '''
  </div> <!-- #{0}-body -->
</div> <!-- #{0} -->
</li>'''.format(google))

    return([out, keys])

google_txt, google_keys = get_google()

with open('google.html', 'w') as f:
    f.write(google_txt)

