
.PHONY: youtube resume update Library

youtube:
	python youtube.py
playlists:
	python itunes.py
resume:
	python resumedate.py

update:
	bash update_web.sh

Library:
	cp ~/Music/iTunes/iTunes\ Music\ Library.xml x/

