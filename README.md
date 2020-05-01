## MP Web App
### Usage
- `./start_mp_web.sh`
### Deployment from Source Code
- add cloud-db-api/config.py and admin-app/config.py
- add admin-app/.flaskenv
- ensure no other apps are listening on port 6543 and 5000
- `export python=<python_command_to_use>`
- `./start_mp_web.sh`