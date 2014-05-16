#!/usr/bin/python

"""
Create tag.txt and posttag.txt for the 
tables to be loaded into MySQL
"""

import pickle

# Read in from pickle
with open('tagtable.txt', 'r') as f:
    td = pickle.load(f)    

# temp to call from execfile() within python shell since
# it has tag_table dictionary already preload in memory
#td = tt

# Create files and output to them
tag_file = open('tag.txt', 'w')
posttag_file = open('posttag.txt', 'w')

tid = 1

for k in td.keys():

    v = td[k]

    tag_file.write("{0}\t{1}\n".format(tid, k))
    
    for pid in v:
        posttag_file.write("{0}\t{1}\n".format(pid, tid))

    tid += 1 

    #if tid == 10:
    #    tid = 0
    #    print "hit enter to continue ..."
    #    raw_input()

print "done creating posttag.txt and tag.txt"
tag_file.close()
posttag_file.close()

print "End of init_tpt.py"
