
.PHONY: youtube itunes-playlist update Library db

youtube:
	python youtube.py
itues-playlists:
	python itunes-playlists.py

update:
	bash update_web.sh

Library:
	cp ~/Music/iTunes/iTunes\ Music\ Library.xml x/

db:
	cp ~/Library/Application\ Support/Google/MusicManager/ServerDatabase.db .

