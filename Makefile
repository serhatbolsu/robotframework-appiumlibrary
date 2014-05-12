.PHONY: help

help:
	@echo targes: generate_doc, 

generate_doc: 
	python -m robot.libdoc ./src/AppiumLibrary/ ./doc/AppimuLibrary.html