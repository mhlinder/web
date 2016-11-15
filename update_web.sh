#!/bin/bash

cd ~/research/web
python resumedate.py
scp resume.html mhlinder@mhlinder.com:~/public_html

