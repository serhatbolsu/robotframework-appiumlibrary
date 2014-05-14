.PHONY: help

help:
	@echo targes: generate_doc, 

generate_doc: 
	python -m robot.libdoc ./src/AppiumLibrary/ ./doc/AppimuLibrary.html

pypi_upload:clean_pyc
	rm -rf src/robotframework_appiumlibrary.egg-info/
	python setup.py sdist upload

clean_pyc:
	find . -iname "*.pyc" -delete
