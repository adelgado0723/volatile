-- Query 10

SELECT STUDENT.name, MIN(ENROLL.grade)
FROM STUDENT, ENROLL
WHERE STUDENT.student_id = ENROLL.student_id
GROUP BY STUDENT.name;


