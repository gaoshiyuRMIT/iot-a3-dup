Cars API Endpoints
==================

.. http:get:: /cars/search
    
    Search for cars.

    **Example request**

    .. sourcecode:: http

        GET /cars/search?car_colour=white&num_seats=4 HTTP/1.0

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": [
                {
                    "body_type": "Sedan",
                    "car_colour": "white",
                    "car_id": 1,
                    "car_model": "Audi S3",
                    "cost_hour": 0.5,
                    "latitude": -37,
                    "longitude": 144,
                    "num_seats": 4,
                    "status": "available",
                    "year": 2015  
                }
            ]
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "InvalidArgument",
            "error_message": "Invalid key(s): bodyy_type"
        }

    :query int car_id: car ID
    :query year: year of production. A list of length 2 (specifying range), or a single int (specifying exact value).
    :query string car_model: car model 
    :query string body_type: body type
    :query num_seats: number of seats. A list of length 2 (specifying range), or a single int (specifying exact value).
    :query string car_colour: car colour
    :query cost_hour: cost in AUD per hour. A list of length 2 (specifying range), or a single decimal number (specifying exact value).

    :>json data: a list of car datas, each json object respresenting a car, with the keys "car_id", "year", "car_model", "body_type", "num_seats", 
                "car_colour", "cost_hour", "latitude", "longitude", "status".
    :>json string error_code: a short code name for the error
    :>json string error_message: readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints


.. http:put:: /cars/(int:car_id)/update

    Update a car's data.

    **Example request**

    .. sourcecode:: http

        PUT /cars/12/update HTTP/1.0
        Content-Type: application/json

        {
            "car_colour": "silver grey"
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
            "error_message": "Invalid key(s): carr_colour"
        }

    :<json int,optional year: year of production
    :<json string,optional car_model: car model
    :<json string,optional body_type: body type
    :<json int,optional num_seats: number of seats
    :<json string,optional car_colour: colour
    :<json decimal,optional cost_hour: cost per hour
    :<json decimal,optional latitude: between -90 and 90
    :<json decimal,optional longitude: between -180 and 180
    :<json string,optional status: one of ``available``, ``booked``
    
    :>json data: has the key "success", which is whether true or false
    :>json error_code: a short name for the error
    :>json error_message: a readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints 

.. http:post:: /cars/add

    Add a new car, and get the inserted car's car_id.

    **Example request**

    .. sourcecode:: http
        
        POST /cars/add HTTP/1.0
        Content-Type: application/json

        {
            "body_type": "Sedan",
            "car_colour": "white",
            "car_model": "Audi S3",
            "cost_hour": 0.5,
            "latitude": -37,
            "longitude": 144,
            "num_seats": 4,
            "status": "available",
            "year": 2015        
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": {
                "car_id": 13
            }
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "InvalidArgument",
            "error_message": "Invalid key(s): carr_colour"
        }

    :<json int year: year of production
    :<json string car_model: car model
    :<json string body_type: body type
    :<json int num_seats: number of seats
    :<json string car_colour: colour
    :<json decimal cost_hour: cost per hour
    :<json decimal latitude: between -90 and 90
    :<json decimal longitude: between -180 and 180
    :<json string status: one of ``available``, ``booked``
    
    :>json data: has the key "car_id", which is the car_id of the newly added car
    :>json error_code: a short name for the error
    :>json error_message: a readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints 
