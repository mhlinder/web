#!/bin/bash

cd ~/research/web
./music.py
scp index.php schema.css resume.php music.php mhlinder@mhlinder.com:~/public_html

