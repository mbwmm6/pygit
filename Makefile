# Определение ОС
ifeq ($(OS),Windows_NT)
	PYTHON := python
	PIP := pip
	RM := rmdir /S /Q
else
	PYTHON := python3.12
	PIP := pip3
	RM := rm -rf
endif

.PHONY: build run clean

build:
<<<<<<< HEAD
	$(PYTHON) setup.py develop
=======
	$(PYTHON) setup.py develop --user
>>>>>>> 0320d363ddf76e1aff124c75654f0248b0083b09

run:
	$(PIP) install -r requirements.txt

clean:
	$(RM) build dist *.egg-info
