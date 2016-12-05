
.PHONY: youtube resume update Library

youtube:
	python youtube.py
resume:
	python resumedate.py
update:
	/home/mlinder/research/web/update_web.sh

Library:
	cp ~/Music/iTunes/iTunes\ Music\ Library.xml x/

