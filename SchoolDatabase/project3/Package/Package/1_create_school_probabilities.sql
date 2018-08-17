DROP TABLE IF EXISTS school_probabilities;
CREATE TABLE school_probabilities
(
  school_code bigint NOT NULL PRIMARY KEY,
  school text NOT NULL,
  probs numeric[] NOT NULL
);