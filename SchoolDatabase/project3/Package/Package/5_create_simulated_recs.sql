DROP TABLE IF EXISTS simulated_recs;

CREATE TABLE simulated_recs
(
  record_id bigint NOT NULL PRIMARY KEY,
  school text NOT NULL,
  grade text NOT NULL
);
