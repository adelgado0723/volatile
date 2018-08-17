-- Query 4 

SELECT name
FROM faculties
WHERE faculty_id IN (SELECT instructor
			FROM   courses
			WHERE semester = 'Spring 2017');


