init:
	$(info Installing dependencies...)
	pip install -r requirements.txt

test:
	$(info Running tests...)
	python -m unittest discover

run:
	$(info Starting service...)
	python run.py

.PHONY: init test
