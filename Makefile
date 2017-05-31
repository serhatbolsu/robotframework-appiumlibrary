.PHONY: help

help:
	@echo targes: version, generate_doc, pypi_upload, clean_pyc, android_demo, ios_demo, demo, unittest, test

generate_doc: 
	VENV/bin/python -m robot.libdoc ./AppiumLibrary/ ./doc/AppiumLibrary.html

update_github:
	version=`python -c "import sys;sys.path.insert(0,'.');import AppiumLibrary;print AppiumLibrary.__version__"`
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

android_demo:
	VENV/bin/pybot ./demo/test_android_demo.txt

ios_demo:
	VENV/bin/pybot ./demo/test_ios_demo.txt

demo:android_demo ios_demo

test_requirements:
    python -m pip install -U -r test_require.txt

unittest: test_requirements
	python setup.py test

test:unittest

coverage:
	py.test --cov AppiumLibrary --cov-report=html tests

version:
	cat AppiumLibrary/version.py
