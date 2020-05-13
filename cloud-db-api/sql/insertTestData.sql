insert into Car (year, car_model, body_type, num_seats, car_colour, cost_hour, latitude, longitude, car_status) values 
(2010, 'Audi A6', "Sedan", 4, 'white', 2.0, -37, 144, 'available');
insert into Car (year, car_model, body_type, num_seats, car_colour, cost_hour, latitude, longitude, car_status) values 
(2008, 'Audi A6', "Sedan", 4, 'black', 2.0, -37, 144, 'available');

insert into User (username, password, fName, lName, email) values 
("janedoe1", "qi8H8R7OM4xMUNMPuRAZxlY.", "Jane", "Doe", "janedoe1@test.com");

insert into Booking (username, car_id, date_booking, time_booking, date_return, time_return, status)
values ("janedoe1", 1, "2019-01-01", "19:00:00", "2019-01-05", "11:00:00", "finished"),
        ("janedoe1", 1, "2020-05-04", "19:00:00", "2020-05-10", "11:00:00", "inProgress"),
        ("janedoe1", 1, "2020-06-01", "19:00:00", "2020-06-05", "11:00:00", "booked");


INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('aspen_admin','Test','Aspen','Forster','Aspen@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('janedoe1','qi8H8R7OM4xMUNMPuRAZxlY.','Jane','Doe','janedoe1@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('janedoe2','qi8H8R7OM4xMUNMPuRAZxlY.','Jane','Doe','janedoe1@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('janedoe5','qi8H8R7OM4xMUNMPuRAZxlY.','Jane','Doe','janedoe1@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('kase_admin','Test','Kase','Fitzpatrick','Kase@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('shiyu_admin','Test','Shiyu','Gao','Shiyu@test.com');
INSERT INTO `User` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('stally_admin','Test','Stally','Duan','Stally@test.com');

