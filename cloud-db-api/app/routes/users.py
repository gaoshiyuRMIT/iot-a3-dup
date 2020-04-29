from . import request, url_for, jsonify
from . import app, usMgr

@app.route("/users/register", methods=["POST"])
def register():
    newUserVal = request.json
    usMgr.addOne(newUserVal)
    result = {"success": 1}
    return jsonify(result)


@app.route("/users/login", methods=["POST"])
def login():
    filt = {
        "username": request.json.get("username"),
        "password": request.json.get("password")
    }
    lst = usMgr.getMany(filt)
    result = {"success": 1}
    if len(lst) == 0:
        result = {"success": 0, "error_code": "IncorrectCredentials", 
                "error_message": "the combination of username and password doesn't exist"}
    return jsonify(result)

