-- Query 1

ALTER TABLE COURSES
ADD semester VARCHAR(20);

UPDATE COURSES
SET semester = 'Spring 2018'
WHERE course_id = 1 OR 
	course_id = 2 OR
	course_id = 3;
	
UPDATE COURSES	
SET semester = 'Fall 2017'
WHERE course_id = 4 OR 
	  course_id = 5;

UPDATE COURSES
SET   semester = 'Spring 2017'
WHERE course_id = 6 OR 
	  course_id = 7; 

-- Query 2

SELECT description
FROM COURSES
WHERE semester LIKE '%2018';

-- Query 3

SELECT description
FROM COURSES
WHERE level = 'grad' AND instructor = (SELECT faculty_id
					   FROM   faculties
					   WHERE name = 'Steven Garden');

-- Query 4 

SELECT name
FROM faculties
WHERE faculty_id IN (SELECT instructor
			FROM   courses
			WHERE semester = 'Spring 2017');

-- Query 5

SELECT COURSES.description, ENROLL.grade
FROM COURSES, ENROLL
WHERE ENROLL.student_id = (SELECT student_id FROM STUDENT WHERE name = 'Alice Wood') AND
		COURSES.course_id = ENROLL.course_id
ORDER BY grade;

-- Query 6

SELECT FACULTIES.name
FROM FACULTIES, COURSES
WHERE FACULTIES.faculty_id = COURSES.instructor 
GROUP BY FACULTIES.name
HAVING COUNT(*) > 1;

-- Query 7

SELECT STUDENT.name, ENROLL.grade
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id AND 
	ENROLL.course_id = (SELECT course_id FROM COURSES WHERE description = 'Fundamentals of Computer Sys.')
ORDER BY ENROLL.grade;

-- Query 8

SELECT name 
FROM FACULTIES
WHERE faculty_id IN (SELECT instructor FROM COURSES WHERE level = 'grad') AND 
	date_of_birth > '19791231'
;

-- Query 9

SELECT STUDENT.name
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id AND
ENROLL.course_id IN (SELECT course_id FROM COURSES WHERE level = 'ugrad')
AND grade = 'B'
GROUP BY STUDENT.name;

-- Query 10

SELECT STUDENT.name, MIN(ENROLL.grade)
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id
GROUP BY STUDENT.name;

-- Query 11

SELECT ENROLL.grade, COUNT(ENROLL.grade)
FROM STUDENT, ENROLL
WHERE STUDENT.name = 'Alice Wood' AND STUDENT.student_id = ENROLL.student_id
GROUP BY ENROLL.grade;

-- Query 12

SELECT name, date_part('year', current_date) - date_part('year', date_of_birth) "student age"
FROM STUDENT
ORDER BY date_of_birth DESC
;

-- Query 13

CREATE TABLE title (
	name VARCHAR(100),
	abbreviation VARCHAR(10)
);

INSERT INTO title (name, abbreviation)
VALUES 
	('Instructor', 'Instr'),
	('Associate Professor', 'AP'),
	('Professor', 'Prof');


UPDATE faculties
SET level = TITLE.abbreviation
FROM TITLE
WHERE FACULTIES.level = TITLE.name
;


