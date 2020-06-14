
# IoT - Assignment 2 

## "Sharing is Car(ing)"

### Team members
- Shiyu Gao s3734720
    - RESTFUL API Shell
    - Google Credentials API
    - RESTFUL API functionality
    - Car Search 
    - Car Booking
- Aspen Forster s3330837
    - Admin-app Shell
    - Google Maps API
    - Login / Registration
    - Input validation
    - Silly art for website
- Kaspian Fitzptrick (Kase) s3630115
    - Facial Recognition
    - Database design and set up
- Xinhuan Duan (Stally) s3713321
    - Agent Pi Console App
    - Credentials Server
    - Socket Programming

### admin-app
admin-app README: [HERE](admin-app/README.md)
#### "admin-app": Booking website to run on the Master Pi
- **<>Service.py** => queries RESTFUL API
- **routes.py** => creates Service objects (see above) and returns results in HTML templates

### cloud-db-api
cloud-db-api README: [HERE](cloud-db-api/README.md)
#### "cloud-db-api": RESTFUL API on the Master Pi - accessed via admin-app
- **<>Manager.py** => creates and executes SQL queries on the Google Cloud SQL instance
- **routes.py** => creates Manager objects (see above) and returns results (to then be passed on to routes.py on admin-app)

### credential_server
Credential Server is run on the Master Pi and listens for the Agent Pi
#### credential server README: [HERE](credential_server/README.md)'

### ap
"ap": Agent Pi Console App allowing customers to unlock/lock cars
#### agent pi README: [HERE](ap/README.md)

### Usage
- For development, you can run the master pi and agent pi from the same machine with this bash script:
- `./start_mp_web.sh`
- the booking web site can be accessed at http://localhost:5000
- the output from flask is redirected admin-app/flask.log and cloud-db-api/flask.log

### Deployment from Source Code
- add cloud-db-api/config.py and admin-app/config.py
- add admin-app/.flaskenv
- ensure no other apps are listening on port 6543 and 5000
- `export python=<python_command_to_use>`
- `./start_mp_web.sh`

### Generating Sphinx Documentation
to generate the API documentation: 
- make sure your virtualenv is activated and has all libraries in requirements.txt installed
- `sphinx-build docs docs/html`
- open docs/html/index.html


### Trello

![Screenshot](trello1.jpg)
![Screenshot](trello2.jpg)
![Screenshot](trello3.jpg)
![Screenshot](trello4.jpg)


### Github

![Screenshot](github1.jpg)
![Screenshot](github2.jpg)
![Screenshot](github4.jpg)
![Screenshot](github3.jpg)
