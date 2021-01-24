PYTHON	:= /usr/bin/env python3.7
PYTHON_PIP  := /usr/bin/env pip3.7

install:
	$(PYTHON_PIP) install -r requirements.txt
