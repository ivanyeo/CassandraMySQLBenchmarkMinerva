#!/usr/bin/python
"""
This script intends to create the Tag mysql table data
as a txt file and then create the PostTag
table data as a txt file as well.
"""
from os import listdir
from os.path import isfile, join, getsize
import sys
import re
import pickle, string

# Configuration
posts_per_query = 10

start_idx = 0
end_idx = start_idx + posts_per_query

# RegEx for hash tags: #tag #another-tag
p = re.compile(r'#[\w|-]+')

# Tags dictionary
tags_dict = dict()

# len(posttags) : 176 630 211
# Strip all tags in text string and add them into tags_dict
# with the given pid
def add_dict(text, pid):
    # Get all tags
    tags = p.findall(text)

    # Sanitize tags: remove leading '#'
    tags = [ t[1:] for t in tags if t[1:] ]

    # Add post.id to tag dictionary
    for tag in tags:
        # if tag exists, append it
        if tags_dict.get(tag):      # Set is too big in memory
            tags_dict.get(tag).append(pid) #.add(pid) #append(pid)
        # if tag doesn't exist, create it and append post.id
        else:
            tags_dict[tag] = [ pid ] #set([ pid ]) #[ pid ]

   

last_pid = 0

with open('post_post.txt', 'r') as file:
    for line in file:
        try:
            pid, text = string.split(line, sep='\t', maxsplit=1)
            pid = int(pid)
        except Exception:
            add_dict(line, last_pid)
            #print "last pid: ", pid
            #print line
            #raw_input()
            continue

        last_pid = pid
        add_dict(text, last_pid) 
        #print "line: ", text 
        #print tags_dict
        #raw_input()

print "process_tags.py DONE :)"

print "Done processing tags ..."
print "writing to output file ... tagtable.txt"

with open('tagtable.txt', 'w') as f:
    pickle.dump(tags_dict, f)            

print "process_tags.py DONE :)"


