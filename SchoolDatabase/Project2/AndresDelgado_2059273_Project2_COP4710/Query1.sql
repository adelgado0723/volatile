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


