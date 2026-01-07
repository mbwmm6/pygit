# Определение ОС
ifeq ($(OS),Windows_NT)
	PYTHON := python
	PIP := pip
	RM := rmdir /S /Q
	VENV_ACTIVATE := .venv\Scripts\activate.bat
else
	PYTHON := python3.12
	PIP := pip3
	RM := rm -rf
	VENV_ACTIVATE := . .venv/bin/activate
endif

.PHONY: build run clean install virt

virt:
	$(PYTHON) -m venv .venv
	@echo "Виртуальное окружение создано."
	@echo "Для активации выполните:"
	@echo "$(VENV_ACTIVATE)"

install:
	$(PYTHON) setup.py develop

build:
	$(PIP) install -r requirements.txt

clean:
	$(RM) build dist *.egg-info .venv
