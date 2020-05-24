Bookings API Endpoints
======================

.. http:get:: /bookings/(int:booking_id)

    Get the data of one booking.

    **Example request**

    .. sourcecode:: http

        GET /bookings/7 HTTP/1.0

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": {
                "booking_id": 7,
                "car_id": 1,
                "date_booking": "2019-01-01",
                "date_return": "2019-01-05",
                "status": "finished",
                "time_booking": "19:00:00",
                "time_return": "11:00:00",
                "username": "janedoe1"
            }
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "MissingKey",
            "error_message": "The specified booking_id does not exist."
        }

    :>json data: a json object representing a booking, with the keys "booking_id", "username", "car_id", "date_booking", "time_booking", "date_return", "time_return", "status". The entries are ordered first by ``status`` ( ``booked`` and ``inProgress`` first) and then by ``booking_id``.
    :>json string error_code: a short code name for the error
    :>json string error_message: readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints

.. http:post:: /bookings/search
    
    Search for bookings.

    **Example request**

    .. sourcecode:: http

        POST /bookings/search HTTP/1.0
        Content-Type: application/json

        {
            "username": "janedoe1",
            "status": "inProgress"
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": [
                {
                    "booking_id": 2,
                    "car_id": 1,
                    "date_booking": "2020-05-04",
                    "date_return": "2019-05-10",
                    "status": "inProgress",
                    "time_booking": "19:58:02",
                    "time_return": "11:00:00",
                    "username": "janedoe1"
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

    :<json int booking_id:
    :<json string username:
    :<json int car_id:
    :<json string date_booking: in iso format, e.g. "2020-06-01"
    :<json string time_booking: in iso format, e.g. "19:58:02"
    :<json string date_return: in iso format, e.g. "2020-06-01"
    :<json string time_return: in iso format, e.g. "19:58:02"
    :<json string status: one of ``booked``, ``inProgress``, ``cancelled``, ``finished``

    :>json data: a list of booking datas, each booking with the keys "booking_id", "username", "car_id", "date_booking", "time_booking", "date_return", "time_return", "status". The entries are ordered first by ``status`` ( ``booked`` and ``inProgress`` first) and then by ``booking_id``.
    :>json string error_code: a short code name for the error
    :>json string error_message: readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints


.. http:put:: /bookings/(int:booking_id)/update

    Update a booking's data.

    **Example request**

    .. sourcecode:: http

        PUT /bookings/3/update HTTP/1.0
        Content-Type: application/json

        {
            "status": "cancelled"
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
            "error_message": "Invalid key(s): statuss"
        }

    :<json string,optional date_booking: in iso format, e.g. "2020-06-01"
    :<json string,optional time_booking: in iso format, e.g. "19:58:02"
    :<json string,optional date_return: in iso format, e.g. "2020-06-01"
    :<json string,optional time_return: in iso format, e.g. "19:58:02"
    :<json string,optional status:

    :>json data: has the key "success", which is whether true or false
    :>json error_code: a short name for the error
    :>json error_message: a readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints 

.. http:post:: /bookings/add

    Add a new booking, and get the inserted booking's booking_id.

    **Example request**

    .. sourcecode:: http
        
        POST /cars/add HTTP/1.0
        Content-Type: application/json

        {
            "car_id": 1,
            "date_booking": "2020-06-01",
            "date_return": "2020-06-05",
            "time_booking": "19:58:02",
            "time_return": "11:00:00",
            "username": "janedoe1"        
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "data": {
                "booking_id": 4
            }
        }

    **Example erroneous response**

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
            "error_code": "MissingKey",
            "error_message": "The specified user does not exist"
        }

    :<json string username: must be of an existing user
    :<json int car_id: must be of an existing car
    :<json string date_booking: in iso format, e.g. "2020-06-01"; must be in the future
    :<json string time_booking: in iso format, e.g. "19:58:02"; must be in the future
    :<json string date_return: in iso format, e.g. "2020-06-01"; must be in the future
    :<json string time_return: in iso format, e.g. "19:58:02"; must be in the future

    :>json data: has the key "booking_id", which is the booking_id of the newly added booking
    :>json error_code: a short name for the error
    :>json error_message: a readable error message
    :statuscode 200: no error
    :statuscode 400: request data is wrong, either with wrong keys or the values do not conform to type/format constraints 
