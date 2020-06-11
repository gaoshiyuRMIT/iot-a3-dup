### usage
- set up virtual environment
  * `python3 -m venv venv`
  * `source venv/bin/activate`
  * `pip install --upgrade pip`
  * `pip install --upgrade -r requirements.txt`
  * create a config.py with the correct config values (refer to config.py.example)
- `flask run`

### references
- [PyMySQL documentation](https://pymysql.readthedocs.io/en/latest/index.html)

### Documentation
to generate the API documentation: 
- make sure your virtualenv is activated and has all libraries in requirements.txt installed
- `sphinx-build docs docs/html`
- open docs/html/index.html
- need conf.py
- some .rst files - one for each page



### Unit Tests
- activate venv
- add details of test database in unittests/test_config.py (refer to unittests/test_config.py.example)
- to execute all the tests: `python -m unittest unittests`
- to execute a particular test case class: e.g. `python -m unittest unittests.db.test_car_manager`
