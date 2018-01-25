
import datetime
import json
import pandas
import requests

## init

base = 'https://api.hypem.com/v2'

secret = {}
with open('secret.txt') as f:
    for l in f.readlines():
        key, value = l.strip().split()
        secret[key] = value

## POST, GET parameters
        
paths = {
    'auth' : '/get_token',
    'fav'   : '/me/favorites'
}

params = {
    'auth' : {
        'username'  : secret['USER'],
        'password'  : secret['PW'],
        'device_id' : '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
    },
    'fav' : {
        'page'     : 0,
        'count'    : 20,
        'hm_token' : None,
        'key'      : secret['KEY']
    }
}

## authentication token

auth = requests.post(base + paths['auth'], data = params['auth'])

params['fav']['hm_token'] = json.loads(auth.text)['hm_token']

## get all favorites
fav = []
while True:
    print('Fetching page ' + str(params['fav']['page']+1))
    res = requests.get(base + paths['fav'], params = params['fav'])
    
    try:
        fav = fav + json.loads(res.text)
        params['fav']['page'] = params['fav']['page'] + 1
        
    except json.JSONDecodeError:
        ## Response is not valid JSON, ie, no more data
        break

pandas.DataFrame(fav).to_csv(datetime.datetime.now().strftime("%Y-%m-%d-hypem.csv"))
