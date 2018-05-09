1. Install [pandoc](http://pandoc.org/)
2. Create a virtualenv, install Python requirements:

```
virtualenv venv
./venv/bin/pip install -r requirements.txt
```
3. Run `convertmdn.py` to convert an MDN page:

```
./venv/bin/python convertmdn.py https://developer.mozilla.org/en-US/docs/Mozilla/Using_the_Mozilla_symbol_server /output/path
```
