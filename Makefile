# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Targets
install: $(VENV)/bin/activate
	. $(VENV)/bin/activate;
	$(PIP) install -r requirements.txt;

serve: $(VENV)/bin/activate
	$(PYTHON) -m flask --app ./src/app/app.py run

test: $(VENV)/bin/activate
	coverage run -m pytest