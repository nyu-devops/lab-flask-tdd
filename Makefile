.PHONY: venv init test run

venv:
	$(info Creating Python 3 virtual environment...)
	python3 -m venv venv

init:
	$(info Installing dependencies...)
	pip install -r requirements.txt

test:
	$(info Running tests...)
	nosetests --with-spec --spec-color

run:
	$(info Starting service...)
	honcho start
