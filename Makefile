.PHONY: help

help:
	@echo targes: generate_doc, 

generate_doc: 
	python -m robot.libdoc ./src/AppiumLibrary/ ./doc/AppimuLibrary.html

pypi_upload:
	python setup.py sdist upload

clean_pyc:
	find . -iname "*.pyc" -delete
