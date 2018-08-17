-- Query 3

SELECT description
FROM COURSES
WHERE level = 'grad' AND instructor = (SELECT faculty_id
					   FROM   faculties
					   WHERE name = 'Steven Garden');


