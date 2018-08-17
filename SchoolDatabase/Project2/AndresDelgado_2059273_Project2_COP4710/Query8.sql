-- Query 8

SELECT name 
FROM FACULTIES
WHERE faculty_id IN (SELECT instructor FROM COURSES WHERE level = 'grad') AND 
	date_of_birth > '19791231'
;
