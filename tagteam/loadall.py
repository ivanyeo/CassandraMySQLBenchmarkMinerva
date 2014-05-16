#!/usr/bin/python
"""
Files that creates loadall.sql that inserts all 68M rows of
posts into the mysql database.

Make sure to run mysql with:
    mysql --local-infile -u minerva -p < loadall.sql

"""
from os import listdir
from os.path import isfile, join, getsize
import sys

TAG_FILE_DIR = 'tagfiles/'

# Get all files
files = [ f for f in listdir(TAG_FILE_DIR) if isfile(join(TAG_FILE_DIR, f)) and getsize(join(TAG_FILE_DIR, f)) ]
files.sort()

#process_file = files[0]
#files = files[:1]
sql_header = """
USE Minerva;

SET autocommit = 0;
"""

sql_indiv_file = """
LOAD DATA LOCAL INFILE '%s'
INTO TABLE post_post
CHARACTER SET utf8
(text, time_created)
SET time_created=NOW();

"""

sql_footer = """
COMMIT;
"""


with open('loadall.sql', 'w') as sqlfile:
    sqlfile.write(sql_header)

    for process_file in files:
        sqlfile.write(sql_indiv_file.replace('%s', join(TAG_FILE_DIR, process_file)))

    sqlfile.write(sql_footer)

