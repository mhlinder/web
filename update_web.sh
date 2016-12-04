#!/bin/bash

cd ~/research/web
./resumedate.py
./music.py
scp index.html schema.css resume.html music.html mhlinder@mhlinder.com:~/public_html

