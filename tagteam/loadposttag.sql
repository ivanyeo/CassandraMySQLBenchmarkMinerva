
USE Minerva;

SET autocommit = 0;
SET foreign_key_checks = 0;

LOAD DATA LOCAL INFILE 'posttag.txt'
INTO TABLE post_posttag
CHARACTER SET utf8
(pid_id, tid_id);

COMMIT;
