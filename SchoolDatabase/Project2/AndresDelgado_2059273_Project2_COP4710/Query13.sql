-- Query 13

CREATE TABLE title (
	name VARCHAR(100),
	abbreviation VARCHAR(10)
);

INSERT INTO title (name, abbreviation)
VALUES 
	('Instructor', 'Instr'),
	('Associate Professor', 'AP'),
	('Professor', 'Prof');


UPDATE faculties
SET level = TITLE.abbreviation
FROM TITLE
WHERE FACULTIES.level = TITLE.name
;


