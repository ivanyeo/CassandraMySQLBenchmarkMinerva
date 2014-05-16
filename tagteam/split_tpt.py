#!/usr/bin/python
"""
This file takes in the pickle dump from 
tag_table_unique_pairs.txt that contains
the unique { 'school': [1,2,3], ... }
dictionary value wrt postid and
decides which files to output for
Athena and Zeus to load up their
tables; posttag and tag
"""

import pickle

# Read in pickle file
#with open('tag_table_unique_pairs.txt', 'r') as f:
#    td = pickle.load(f)

# Process output
tid = 1

# Split value of half the MySQL IDs to Athena and Zeus
split = 59976390  

# Open output files
a_posttag = open('a_posttag.txt', 'w')
a_tag = open('a_tag.txt', 'w')
z_posttag = open('z_posttag.txt', 'w')
z_tag = open('z_tag.txt', 'w')

# Request to write to output file
a_write = 0
z_write = 0

for k in td.keys():
    v = td[k]

    a_write = 0
    z_write = 0

    for pid in v:
        if pid <= split:
            a_posttag.write("{0}\t{1}\n".format(pid, tid))
            a_write = 1
        else:
            z_posttag.write("{0}\t{1}\n".format(pid, tid))
            z_write = 1

    # If we have requested to copy
    if a_write:
        a_tag.write("{0}\t{1}\n".format(tid, k))

    if z_write:
        z_tag.write("{0}\t{1}\n".format(tid, k))

    tid += 1

    #print "Done processing key: ", k
    #print "Hit any key to move to the next key."
    #raw_input()

# Ouptut to nohup.out
print "Done Processing files"
print "Closing output files now ..."

# Close output files 
a_posttag.close()
a_tag.close()
z_posttag.close()
z_tag.close()

# Output to nohup.out 
print "Done writing files."
