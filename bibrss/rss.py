
## Number of most recent books to show from the RSS feed in secret_rss.txt
nprint = 10

from bs4 import BeautifulSoup
from re import sub
from requests import get

with open('secret_rss.txt') as f:
    r = get(f.read().strip())
soup = BeautifulSoup(r.text, 'lxml')

items = soup.findAll('item')

formats = [r' *\[EPUB\] *', r' *\[PDF\] *', r' *\[MOBI\] *',
           r' *\[[0-9]{4}\] *',
           r' *\[RETAIL\] *']

for item in items[:10]:
    title = item.title.text
    for f in formats:
        title = sub(f, '', title)
    title = title.strip()
    title = title.split(' -  by ')
    print('{0}, by {1}'.format(title[0], title[1]))

