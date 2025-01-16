# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Targets
install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

run: $(VENV)/bin/activate
	$(PYTHON) -m flask --app ./src/app/app.py run