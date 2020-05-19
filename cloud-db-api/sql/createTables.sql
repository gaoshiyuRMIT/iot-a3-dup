USE test;

CREATE TABLE IF NOT EXISTS User ( 
    username VARCHAR(32) not null, 
    password VARCHAR(255) not null,
    fName VARCHAR(32) not null,
    lName VARCHAR(32) not null,
    email VARCHAR(255) not null,   
    CONSTRAINT PK_User PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS Car ( 
    car_id INT not null auto_increment, 
    year INT not null, 
    car_model VARCHAR(32) not null,
    body_type VARCHAR(32) not null,
    num_seats INT not null, 
    car_colour VARCHAR(32) not null,
    cost_hour  float(6,2) not null, 
    latitude float(38, 20), 
    longitude float(38, 20), 
    car_status VARCHAR(32) not null,  
    CONSTRAINT PK_Car PRIMARY KEY (car_id)
);

CREATE TABLE IF NOT EXISTS Booking ( 
    booking_id INT not null AUTO_INCREMENT, 
    username VARCHAR(32) not null,
    car_id INT, 
    date_booking DATE not null,
    time_booking TIME not null,
    date_return DATE not null,
    time_return TIME not null,
    status VARCHAR(32) not null default 'booked',
    CONSTRAINT PK_Booking PRIMARY KEY (booking_id),
    INDEX (username),
    INDEX (car_id),
    constraint FK_Booking_username foreign key (username) references User(username)
        ON UPDATE CASCADE ON DELETE CASCADE,
    constraint FK_Booking_car_id foreign key (car_id) references Car(car_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);
