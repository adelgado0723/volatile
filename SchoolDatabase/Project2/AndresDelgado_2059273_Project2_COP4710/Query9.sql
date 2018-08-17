-- Query 9

SELECT STUDENT.name
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id AND
ENROLL.course_id IN (SELECT course_id FROM COURSES WHERE level = 'ugrad')
AND grade = 'B'
GROUP BY STUDENT.name;


