# webdir = '/home/mhlinder/www/'
webdir = '.'

f = open(webdir + 'resume.html', 'r')
text = f.read()
f.close()

import datetime
from re import compile

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

g1 = 'https://github.com/mhlinder">'
g2 = '</a>'
q = compile('(' + g1 + ')[A-Z 0-9]*(' + g2 + ')')
text = q.sub(g1 + tomorrow.strftime("%d %b %y").upper() + g2, text)

g1 = 'https://twitter.com/mhlinder">'
g2 = '</a>'
q = compile('(' + g1 + ')[A-Z 0-9]*(' + g2 + ')')
text = q.sub(g1 + today.strftime("%d %b %y").upper() + g2, text)

f = open(webdir + 'resume.html', 'w')
f.write(text)
f.close()
