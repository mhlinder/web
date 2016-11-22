#!/bin/bash

cd ~/research/web
./resumedate.py
./music.py
scp index.html resume.html music.html schema.css mhlinder@mhlinder.com:~/public_html

