-- Query 5

SELECT COURSES.description, ENROLL.grade
FROM COURSES, ENROLL
WHERE ENROLL.student_id = (SELECT student_id FROM STUDENT WHERE name = 'Alice Wood') AND
		COURSES.course_id = ENROLL.course_id
ORDER BY grade;


