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

install:
	$(PYTHON) setup.py develop

build:
	$(PIP) install -r requirements.txt

clean:
	$(RM) build dist *.egg-info
