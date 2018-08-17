-- Query 7

SELECT STUDENT.name, ENROLL.grade
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id AND 
	ENROLL.course_id = (SELECT course_id FROM COURSES WHERE description = 'Fundamentals of Computer Sys.')
ORDER BY ENROLL.grade;


