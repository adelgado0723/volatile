-- Task 1

-- Query 1

CREATE TABLE STUDENT
(
student_id INT,
name VARCHAR(50) NOT NULL,
date_of_birth DATE,
address VARCHAR(30),
email VARCHAR(30),
level VARCHAR(30) NOT NULL,
PRIMARY KEY(student_id),
Unique(email)
);

CREATE TABLE FACULTIES
(
faculty_id INT,
name VARCHAR(50) NOT NULL,
date_of_birth DATE,
address VARCHAR(30),
email VARCHAR(30),
level VARCHAR(30) NOT NULL,
PRIMARY KEY(faculty_id),
Unique(email)
);

CREATE TABLE COURSES
(
course_id INT,
description VARCHAR(100) NOT NULL,
level VARCHAR(30) NOT NULL,
instructor INT,
PRIMARY KEY(course_id),
FOREIGN KEY(instructor) REFERENCES FACULTIES(faculty_id)
);

CREATE TABLE ENROLL
(
student_id INT REFERENCES STUDENT(student_id),
course_id INT REFERENCES COURSES(course_id),
grade VARCHAR(2),
PRIMARY KEY(student_id, course_id)
);

-- Query 2

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(1, 'Alice Wood', '06/15/1993', '5637 NW 41 ST', 'awood001@cis.fiu.edu', 'ugrad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(2, 'Henrie Cage', '04/24/1994', '1443 NW 7 ST', 'hcage001@cis.fiu.edu', 'ugrad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(3, 'John Smith', '01/09/1995', '731 NW 87 AVE', 'jsmit005@cis.fiu.edu', 'ugrad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(4, 'Franklin Wong', '12/08/1995', '638 NW 104 AVE', 'fwong001@cis.fiu.edu', 'ugrad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(5, 'Jennifer King', '11/08/1998', '3500 W Flagler ST', 'jking001@cis.fiu.edu', 'ugrad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(6, 'Richard Young', '12/05/1995', '778 SW 87 AVE', 'ryoun001@cis.fiu.edu', 'grad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(7, 'Robert Poore', '08/22/1996', '101 SW 8 ST', 'rpooj001@cis.fiu.edu', 'grad');

INSERT INTO STUDENT (student_id, name, date_of_birth, address, email, level)
VALUES			(8, 'Joyce English', '07/31/1999', '8421 SW 109 AVE', 'jengl001@cis.fiu.edu', 'grad');


INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (1, 'George Blunt', '08/13/1979', '11345 SW 56th ST', 'bluns@cs.fiu.edu', 'Instructor');

INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (2, 'Thomas Taylor', '05/24/1988', '4467 NW 8 ST', 'taylt@cs.fiu.edu', 'Instructor');

INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (3, 'Daniel Evans', '10/07/1979', '8754 SW 134 TER', 'evand@cs.fiu.edu', 'Professor');

INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (4, 'Ramesh Nara', '09/15/1982', '5631 SW 72 ST', 'narar@cs.fiu.edu', 'Professor');

INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (5, 'Steven Garden', '09/18/1975', '1277 SW 87 AVE', 'gards@cs.fiu.edu', 'Associate Professor');

INSERT INTO FACULTIES (faculty_id, name, date_of_birth, address, email, level)
VALUES		      (6, 'William Parre', '11/22/1976', '1570 NE 127 AVE', 'parrw@cs.fiu.edu', 'Instructor');


INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (1, 'Fundamentals of Computer Sys.', 'ugrad', 1);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (2, 'Software Engineering I', 'ugrad', 2);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (3, 'Computer Programming I', 'ugrad', 2);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (4, 'Introduction to Algorithms', 'grad', 4);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (5, 'Operating Systems', 'grad', 5);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (6, 'Software Design', 'grad', 6);

INSERT INTO COURSES (course_id, description, level, instructor)
VALUES		    (7, 'Advanced Database', 'grad', 5);


INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (1, 1, 'A');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (1, 2, 'B');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (1, 3, 'A');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (3, 1, 'F');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (3, 3, 'C');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (4, 3, 'NA');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (5, 1, 'B');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (6, 6, 'C'); 

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (6, 7, 'B');

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (7, 7, 'B');



-- Task 2

-- Query 1

INSERT INTO ENROLL (student_id, course_id, grade)
VALUES		   (2, 1, 'D'),
		   (2, 2, 'NA'),
		   (2, 3, 'F'),
		   (8, 5, 'A'),
		   (8, 7, 'A');

-- Query 2

DELETE FROM enroll WHERE grade = 'NA';


-- Query 3

ALTER TABLE courses
ADD semester VARCHAR(12);


-- Query 4

UPDATE enroll
SET grade = 'C'
WHERE student_id IN
	(SELECT student_id
	FROM student
	WHERE name = 'Henrie Cage'
	)

AND course_id IN
	(SELECT course_id
	FROM courses
	WHERE description = 'Computer Programming I'
	)
;

-- Query 5

ALTER TABLE courses 
ADD CONSTRAINT restrict_delete 
FOREIGN KEY (instructor) 
REFERENCES faculties(faculty_id) ON DELETE RESTRICT;

-- Query 6

ALTER TABLE enroll
ALTER COLUMN grade
SET NOT NULL;

-- Query 7

COPY enroll
TO 'Enroll.csv' DELIMITER ',' CSV HEADER;



