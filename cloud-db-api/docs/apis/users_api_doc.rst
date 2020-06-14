Users API Endpoints
===================

.. http:post:: /users/register
    
    Register a new user.

    **Example request**

    .. sourcecode:: http

        POST /users/register HTTP/1.0
        Content-Type: application/json

        {
            "username": "shiyugao1",
            "password": "qi8H8R7OM4xMUNMPuRAZxlY.",
            "fName": "Shiyu",
            "lName": "Gao",
            "email": "shiyugao1@test.css.com"
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": {
                "success": true
            }
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "InvalidArgument",
            "error_message": "Invalid key(s): usermame"
        }

    :<json username: username
    :<json password: hashed password
    :<json fName: first name
    :<json lName: last name
    :<json email: email
    :>json data: has the key "success", which has a boolean value, indicating whether the new user is successfully added
    :>json error_code: a short code name for the error
    :>json error_message: readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints


.. http:post:: /users/login

    Check the log-in credentials.

    **Example request**

    .. sourcecode:: http

        POST /users/login HTTP/1.0
        Content-Type: application/json

        {
            "username": "shiyugao1",
            "password": "qi8H8R7OM4xMUNMPuRAZxlY."
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": {
                "success": true
            }
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "InvalidArgument",
            "error_message": "Invalid key(s): passsword"
        }

    :<json username: username
    :<json password: hashed password
    :>json data: has the key "success", which is whether true or false, indicating whether the credential-check has passed
    :>json error_code: a short name for the error
    :>json error_message: a readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints 

        