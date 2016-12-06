#!/bin/bash

cd ~/research/web
./youtube.py
scp index.php schema.css resume.php music.php x/playlists.html youtube.html mhlinder@mhlinder.com:~/public_html

