.PHONY: help

help:
	@echo targes: version, generate_doc, pypi_upload, clean_pyc, andriod_demo, ios_demo, demo, unittest, test

generate_doc: 
	VENV/bin/python -m robot.libdoc ./src/AppiumLibrary/ ./doc/AppimuLibrary.html

update_github:
	version=`python -c "import sys;sys.path.insert(0,'src');import AppiumLibrary;print AppiumLibrary.__version__"`
	git tag $version
	git push origin $version
	git push origin master
	git checkout gh-pages
	git merge master
	git push origin gh-pages
	git checkout master	


pypi_upload:clean_pyc
	rm -rf src/robotframework_appiumlibrary.egg-info/
	VENV/bin/python setup.py sdist upload
	@echo https://pypi.python.org/pypi/robotframework-appiumlibrary/

clean_pyc:
	find . -iname "*.pyc" -delete
	find . -iname "__pycache__" | xargs rm -rf {} \;

andriod_demo:
	VENV/bin/pybot ./demo/test_andriod_demo.txt

ios_demo:
	VENV/bin/pybot ./demo/test_ios_demo.txt

demo:andriod_demo ios_demo

unittest:
	py.test -s tests 

test:unittest

coverage:
	py.test --cov AppiumLibrary --cov-report=html tests

version:
	cat src/AppiumLibrary/version.py
