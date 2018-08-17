DROP TABLE IF EXISTS grade_values;
CREATE TABLE grade_values
(
  id integer NOT NULL PRIMARY KEY,
  score text NOT NULL,
  grade text NOT NULL
);