-- Query 11

SELECT ENROLL.grade, COUNT(ENROLL.grade)
FROM STUDENT, ENROLL
WHERE STUDENT.name = 'Alice Wood' AND STUDENT.student_id = ENROLL.student_id
GROUP BY ENROLL.grade;


