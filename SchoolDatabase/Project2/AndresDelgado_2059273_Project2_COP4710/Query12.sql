-- Query 12

SELECT name, date_part('year', current_date) - date_part('year', date_of_birth) "student age"
FROM STUDENT
ORDER BY date_of_birth DESC
;
