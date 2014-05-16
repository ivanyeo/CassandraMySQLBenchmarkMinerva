
USE Minerva;

SET autocommit = 0;

LOAD DATA LOCAL INFILE 'tagfiles/tagfile1.txt' 
INTO TABLE post_post
CHARACTER SET utf8
(text, time_created)
SET time_created=NOW();

COMMIT;

