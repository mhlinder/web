#!/usr/bin/env python3

import datetime
from string import Template

with open('resume.tmp', 'r') as f:
    s = Template(f.read())

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

s = s.substitute(tomorrow = tomorrow.strftime("%d %b %y").upper(),
                 today = today.strftime("%d %b %y").upper())

with open('resume.html', 'w') as f:
    f.write(s)

