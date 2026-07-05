venv:
	python -m venv .

install:
	Scripts\pip install -r requirements.txt

run:
	Scripts\python src/main.py

setup: venv install