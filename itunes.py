
from collections import defaultdict
from pyItunes import Library

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

numbers_pl = defaultdict(dict)
for cid in numbers:
    pl = lookup[cid]
    p = pl['playlist']

    songs = [format_song(s) for s in p.tracks]
    parent = pl['parents'][0]

    numbers_pl[parent][p.name] = songs

seasons = sorted(numbers_pl.keys())
with open('x/playlists.md', 'w') as f:
    for season in seasons:
        f.write('\n\n# {0}'.format(season))
        playlists = numbers_pl[season]
        for pn in sorted(playlists.keys()):
            songs = playlists[pn]
            p_txt = '\n'.join(['* {0}'.format(s) for s in songs])
            f.write('\n\n\n## {0}\n\n{1}'.format(pn, p_txt))

    f.write('\n\n')

