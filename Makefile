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

andriod_demo:
	pybot ./demo/test_andriod_demo.txt

ios_demo:
	pybot ./demo/test_ios_demo.txt

demo:andriod_demo ios_demo

unittest:
	py.test tests

test:unittest

version:
	cat src/AppiumLibrary/version.py