INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (1,2010,'Audi A6','Sedan',4,'white',2.00,-37.38217926025390600000,144.25573730468750000000,'inUse');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (2,2008,'Audi A6','Sedan',4,'black',2.00,-37.08553314208984400000,144.55895996093750000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (3,2010,'Audi A6','Sedan',4,'white',2.00,-37.79268646240234400000,144.60922241210938000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (4,2010,'Audi A6','Sedan',4,'white',2.00,-37.08375930786133000000,144.93452453613280000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (5,2008,'Audi A6','Sedan',4,'black',2.00,-37.54005432128906000000,144.51052856445312000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (6,1992,'Ford Fiesta','Hatchback',2,'green',0.50,-37.31035232543945000000,144.99191284179688000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (7,2004,'Ski-Doo MX Z 600 TRAIL','Sedan',4,'silver',10.40,-36.98672485351562500000,144.17018127441406000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (8,2001,'Honda SA50 ELITE SR','Sedan',2,'gold',20.00,-37.00000000000000000000,144.00000000000000000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (9,2015,'Kenworth T270','Sedan',4,'yellow',4.40,-37.96701049804687500000,144.04505920410156000000,'available');
INSERT INTO `Car` (`car_id`,`year`,`car_model`,`body_type`,`num_seats`,`car_colour`,`cost_hour`,`latitude`,`longitude`,`car_status`) VALUES (10,2004,'Victory KINGPIN','Sedan',4,'yellow',5.60,-36.98672485351562500000,144.17018127441406000000,'available');

INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('aspen1','Test','Aspen','Forster','aspenforster@gmail.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('aspen2','$5$rounds=1000$gLmOiSOuv4v.QcNC$P1VsaQ9lT2abD2pv2lf6zcPSDV7eSDf1uEh15p3vjGA','Aspen','Forster','aspenforster@gmail.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('aspen_admin','Test','Aspen','Forster','Aspen@test.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('kase_admin','$5$rounds=1000$Vk9Jo4IAqCj5nCsx$kCwG0jfr87Ndyu34y3Ajj7dLhconi83xSaPuGfnuX7A','Kase','Fitz','kase@test.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('sddasdasdads','asdasdaDSA','Aspen','Forster','aspenforster@gmail.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('shiyu_admin','$5$rounds=1000$xHvtszBgCAgnn4aq$yJHUxh78iVHeaRnGx09ucuAa3MrgaTwthHeJ7PaCOx.','Shiyu','Gao','shiyu@test.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('shiyu_test','$5$rounds=1000$ppbpsWHm0ftLKivL$T444TG2x.ci/OgiW/Bplos4CvkGYxzF2.IbR/f89LVC','Shiyu','Gao','shiyu@test1.com');
INSERT INTO `` (`username`,`password`,`fName`,`lName`,`email`) VALUES ('stally_admin','$5$rounds=1000$y6y.eQ8ZAPsEMmMI$8OWXwBKS4BkiXE4VAQUkKLWKBQElx4j5veRctERCwRD','Stally','Neil','stally@test.com');

insert into Booking (username, car_id, date_booking, time_booking, date_return, time_return, status)
values ("shiyu_admin", 1, "2019-01-01", "19:00:00", "2019-01-05", "11:00:00", "finished"),
        ("shiyu_admin", 1, "2020-05-04", "19:00:00", "2020-05-10", "11:00:00", "inProgress"),
        ("shiyu_admin", 1, "2020-06-01", "19:00:00", "2020-06-05", "11:00:00", "booked");

INSERT INTO 'Employee' ('username', 'password', 'fName', 'lName', 'email', 'role') VALUES ('emp1', '$5$rounds=1000$oZLmSIdjgrXyZdna$AlnLGwFyQgWLNorc61uZs2XanirgttrCJT2f56.yX60', 'kase', 'fitz', 'fitz@gmail.com', 'admin');
INSERT INTO 'Employee' ('username', 'password', 'fName', 'lName', 'email', 'role') VALUES ('emp2', '$5$rounds=1000$oZLmSIdjgrXyZdna$AlnLGwFyQgWLNorc61uZs2XanirgttrCJT2f56.yX60', 'kase', 'fitz', 'fitz@gmail.com', 'manager');
INSERT INTO 'Employee' ('username', 'password', 'fName', 'lName', 'email', 'role') VALUES ('emp3', '$5$rounds=1000$oZLmSIdjgrXyZdna$AlnLGwFyQgWLNorc61uZs2XanirgttrCJT2f56.yX60', 'kase', 'fitz', 'fitz@gmail.com', 'engineer');