### usage
- set up virtual environment
  * `python3 -m venv venv`
  * `source venv/bin/activate`
  * `pip install --upgrade pip`
  * `pip install --upgrade -r requirements.txt`
  * create a config.py with the correct config values (refer to config.py.example)
  * create a .flaskenv with the correct config values (refer to .flaskenv.example)
  * download credentials.json from google API console (see below & refer to credentials.json.example)
- `flask run --host=0.0.0.0`

### Google API Credentials
- go to [google api console](https://console.developers.google.com/apis) -> select a project -> Credentials -> create credentials -> choose OAuth Client ID -> configure consent screen -> choose web application -> in "Authorised Javascript Origins" fill in the domain name (e.g. http://localhost:6060, http://raspberrypi.local:6060) from which your app will call the google APIs -> click "create"
- download json and store as "crendentials.json" in working directory

### references
- [PyMySQL documentation](https://pymysql.readthedocs.io/en/latest/index.html)

