VENV = venv
PYTHON = python3.10
PIP = $(VENV)/bin/pip
PORT = 8501

run: $(VENV)/bin/activate
	$(VENV)/bin/python -m streamlit run app.py --server.port $(PORT)

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(VENV) 
	find -iname "*pyc" -delete