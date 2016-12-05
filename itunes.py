
from pyItunes import Library

def get_names(ids):
    return([lookup[x]['name'] for x in ids])

l = Library('x/iTunes Music Library.xml')
playlists = [x for x in l.getPlaylistNames() if x != 'iTunes\xa0U']

# Key is playlist persistent ID
lookup = dict()
name_lookup = dict()
# Root playlists / folders
roots = list()
# List of IDs whose parent does not exist when they are initially read
parentless = list()

# Format playlist entry lookup, especially with IDs connecting
# children playlists to parents
for pn in playlists:
    p = l.getPlaylist(pn)

    cid = p.playlist_persistent_id
    pid = p.parent_persistent_id
    name = p.name

    lookup[cid] = { 'playlist' : p,
                    'name'     : name,
                    'id'       : cid,      # Current ID
                    'pid'      : pid,      # Parent ID
                    'children' : list() }

    name_lookup[name] = cid

    if pid is None:
        roots.append(cid)
    else:
        if pid not in lookup.keys():
            print('error')
            parentless.append(cid)
        else:
            lookup[pid]['children'].append(cid)
            
for pn in playlists:
    cid = name_lookup[pn]
    p = lookup[cid]
    pid = p['pid']
    parents = list()
    while pid is not None:
        parent = lookup[pid]
        parents.append(parent['name'])
        pid = parent['pid']
    if len(parents) > 0:
        lookup[cid]['parents'] =  parents
        lookup[cid]['root'] =  parents[-1]
    else:
        lookup[cid]['parents'] = None
        lookup[cid]['root'] = None

for pn in playlists:
    cid = name_lookup[pn]
    p = lookup[cid]
    if not p['playlist'].is_folder:
        print(p['root'])

