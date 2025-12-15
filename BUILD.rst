Short version of the release procedures ..

#. Add new contributors to README
#. Update version
#. Update CHANGES
#. Rebuild keyword documentation if needed::

     libdoc AppiumLibrary docs/AppiumLibrary.html

#. Commit documentation::

     git commit -m "Generated docs for version $VERSION" docs/AppiumLibrary.html
     git push

#. Build release files::

     # clean dist/ folder
     rm -Rf dist
     # build release files
     python -m build
     # verify
     ls dist

#. Deploy to PyPI::

     twine upload dist/*

#. tag code::

      git tag -a v$VERSION -m "Release $VERSION"
      git push --tags

#. Create release notes
