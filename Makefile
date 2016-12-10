
.PHONY: youtube resume update Library

youtube:
	python youtube.py
resume:
	python resumedate.py
>>>>>>> d9ce8eb93f272e0b21babcca3816e4b2df6df82c
update:
	bash update_web.sh

Library:
	cp ~/Music/iTunes/iTunes\ Music\ Library.xml x/

