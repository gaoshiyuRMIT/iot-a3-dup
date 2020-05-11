## MP Web App
### Usage
- `./start_mp_web.sh`
- the web site can be accessed at http://localhost:5000
- the output from flask is redirected admin-app/flask.log and cloud-db-api/flask.log
### Deployment from Source Code
- add cloud-db-api/config.py and admin-app/config.py
- add admin-app/.flaskenv
- ensure no other apps are listening on port 6543 and 5000
- `export python=<python_command_to_use>`
- `./start_mp_web.sh`

### [cloud-db-api README](cloud-db-api/README.md)
### [admin-app README](admin-app/README.md)

### Codebase structure Notes 
#### "admin-app"
- *<>Service.py* => queries and posts results from RESTful API
- *routes.py* => creates Service objects (see above) and returns results in HTML templates

#### "cloud-db-api"
- *<>Manager.py* => creates and executes SQL queries
- *routes.py* => creates Manager objects (see above) and returns results (to then be passed on to routes.py on admin-app)
