#!/usr/bin/env python3

outfile = 'playlists.html'

from collections import defaultdict
from pyItunes import Library
from string import ascii_letters, digits

from gmusicapi import Mobileclient
from re import compile
from sqlite3 import connect

alphanum = ascii_letters + digits + '-'

### iTunes extract

# Get playlist names, given a list of IDs
def get_names(ids):
    return([lookup[x]['name'] for x in ids])

# Get direct parent folder, given a list of IDs
def get_parent(ids):
    return([lookup[x]['parents'][0] for x in ids])

# Format a song based on title and artist
title_by_artist = "'{0}' - {1}"  ## 'Song' by So and so
def format_song(song):
    if song.artist is None:
        return("'{0}'".format(song.name))
    else:
        return(title_by_artist.format(song.name, song.artist))

l = Library('x/iTunes Music Library.xml')
playlists = [x for x in l.getPlaylistNames() if x != 'iTunes\xa0U']

# Key is playlist persistent ID
lookup = dict()
name_lookup = dict()

lounge = list()
numbers = list()

# Populates playlist entres in `lookup` by ID, which can be obtained
# from a playlist name using `name_lookup`.
for pn in playlists:
    p = l.getPlaylist(pn)

    cid = p.playlist_persistent_id
    pid = p.parent_persistent_id
    name = p.name

    pp = { 'playlist' : p,
           'name'     : name,
           'id'       : cid,      # Current ID
           'pid'      : pid,      # Parent ID
           'children' : list() }

    name_lookup[name] = cid

    # Register as a child of a parent
    if pid in lookup.keys():
        lookup[pid]['children'].append(cid)

    # Identify list of parent nodes, in order, until the root node
    parents = list()
    while pid is not None:
        parent = lookup[pid]
        parents.append(parent['name'])
        pid = parent['pid']

    if len(parents) == 0:
        pp['parents'] = None
        pp['root'] = None
    else:
        pp['parents'] =  parents
        root = parents[-1]
        pp['root'] = root

        if not p.is_folder:
            if root == 'lounge':
                lounge.append(cid)
            elif root == 'numerology':
                numbers.append(cid)

    lookup[cid] = pp

# Populate song lists for numbered playlists
numbers_pl = defaultdict(dict)
for cid in numbers:
    pl = lookup[cid]
    p = pl['playlist']

    songs = [format_song(s) for s in p.tracks]
    parent = pl['parents'][0]

    numbers_pl[parent][p.name] = songs

# All playlist names that need to be hide-able
keys = list()

# For each period (a season), add a list of all playlists
seasons = sorted(numbers_pl.keys())
with open(outfile, 'w') as f:
    for season in seasons:
        # Header for the season
        keys.append(season)
        f.write('''

<li><div id="{0}">
  <strong><a href="#" id="{0}-title">{1}</a></strong>
  <div id="{0}-body" style="display: none;">\n<ul class="space-before space-after">'''.format(season, season.replace('--', '&ndash;')))

        # Loop over playlists
        season_pls = numbers_pl[season]
        for pn in sorted(season_pls.keys()):
            songs = season_pls[pn]

            # Record songs
            entries = list()
            for i in range(len(songs)):
                s = songs[i]
                entries.append('<li>{1}</li>'.format(i+1, s))

            p_txt   = '\n'.join(entries)
            p_title = ''.join([c for c in pn.replace(' ', '-') if c in alphanum])
            keys.append(p_title)
            f.write('''


    <li><div id="{1}">
      <a href="#" id="{1}-title">{0}</a>

      <div id="{1}-body" style="display: none;">
        <ol class="space-before space-after">
          {2}
        </ol>
      </div> <!-- #{1}-body -->
    </div> <!-- #{1} -->'''.format(pn, p_title, p_txt))

        f.write('''
  </div> <!-- #{0}-body -->
</div> <!-- #{0} -->
</li>'''.format(season))


### Google Play extract

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

# All playlists to record start with a three digit integer
format_check = compile('^[0-9]{3}(?::|$)')
# Note the clash between the search string ':' and the syntax of
# non-capturing groups in regexes (?:...)

inplaylists = api.get_all_user_playlist_contents()
playlists = [p for p in inplaylists if format_check.search(p['name']) is not None]
playlists = sorted(playlists, key = lambda k: k['name'])
playlists = playlists[1:] + playlists[:1]

google = '2017-01--'
keys.append(google)

with(open(outfile, 'a')) as f:
    f.write('''


<li><div id="{0}">
  <strong><a href="#" id="{0}-title">{1}</a></strong>
  <div id="{0}-body" style="display: none;">\n<ul class="space-before space-after">'''.format(google, google.replace('--', '&ndash;')))

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
        f.write('''

    <li><div id="{1}">
      <a href="#" id="{1}-title">{0}</a>

      <div id="{1}-body" style="display: none;">
    <ol class="space-before space-after">
      {2}
    </ol>
  </div> <!-- #{1}-body -->
</div> <!-- #{1} -->
</li>'''.format(pn, p_title, p_txt))

    f.write('''
  </div> <!-- #{0}-body -->
</div> <!-- #{0} -->
</li>'''.format(google))

### END

with open(outfile, 'a') as f:
    f.write('''

    <li class="space-before"><div id="flood-text">[<a href="#" id="flood">flood the gates</a>]</div></li>
</ul>

<script>
    var playlists = ['youtube', 'some-songs', '{0}'];
    for (i = 0; i < playlists.length; i++) {{
        var pl_key = playlists[i];
        function toggle_visible(x) {{
            var in_key = x.target.id.split('-title')[0],
                key = document.getElementById(in_key.concat('-body'));

            if (key.style.display == 'none') {{
                key.style.display = 'block';
            }} else {{
                key.style.display = 'none';
            }}
        }}
        document.getElementById(pl_key.concat('-title'))
            .addEventListener('click', function(e) {{ e.preventDefault(); toggle_visible(e); }});
    }}
    
    var flooded = false;
    function toggle_all() {{
        for (i = 0; i < playlists.length; i++) {{
            var pl_key = playlists[i];
            key = document.getElementById(pl_key.concat('-body'));

            if (!flooded) {{
                key.style.display = 'block';
            }} else {{
                key.style.display = 'none';
            }}
        }}

        key = document.getElementById('flood-text');
        if (flooded) {{
            flooded = false;
        }} else {{
            flooded = true;
        }}
    }}
    document.getElementById('flood')
        .addEventListener('click', function(e) {{ e.preventDefault(); toggle_all(); }});
</script>

'''.format("', '".join(keys)))

