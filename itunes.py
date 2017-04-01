#!/usr/bin/env python3

from collections import defaultdict
from pyItunes import Library
from string import ascii_letters, digits

alphanum = ascii_letters + digits + '-'

# Get playlist names, given a list of IDs
def get_names(ids):
    return([lookup[x]['name'] for x in ids])

# Get direct parent folder, given a list of IDs
def get_parent(ids):
    return([lookup[x]['parents'][0] for x in ids])

# Format a song based on title and artist
def format_song(song):
    if song.artist is None:
        return("'{0}'".format(song.name))
    else:
        return("'{0}' - {1}".format(song.name, song.artist))

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

# For each period (a season), add a list of all playlists
seasons = sorted(numbers_pl.keys())
with open('playlists.html', 'w') as f:
    keys = list()
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

    f.write('''

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
</script>

'''.format("', '".join(keys)))

