#!/usr/bin/python

from os import listdir
from os.path import isfile, join, getsize
from post.models import Post, Tag, PostTag
import sys

TAG_FILE_DIR = 'tagfiles/'

# Get all files
files = [ f for f in listdir(TAG_FILE_DIR) if isfile(join(TAG_FILE_DIR, f)) and getsize(join(TAG_FILE_DIR, f)) ]
files.sort()

#process_file = files[0]

#files = files[:1]
for process_file in files:
    # Process file line by line
    with open(join(TAG_FILE_DIR, process_file), 'r') as f:
        for line in f:
            # Create post
            if len(line) > 140:
                # dump the line if it's great than 140
                continue
                #print "LINE EXCEED: ", line
                #sys.exit(1)

            try:
                post = Post.objects.create(text = line)
            except Exception:
                print "Unable to create Post: ", line
                continue

            # Get words in the line
            words = line.split()

            # Get hash tags
            for w in words:
                if w[0] == '#':
                    w = w[1:]

                    # If w is not an empty string: ''
                    #if not w:
                    # Create tag if it doesn't exist
                    try:
                        tag = Tag.objects.get_or_create(value = w)[0]

                        try:
                            # Insert post-tag tuple
                            post_tag = PostTag.objects.create(pid = post, tid = tag)
                        except Exception:
                            print "Unable to create PostTag: ", post, ", ", tag
                            continue

                    except Exception:
                        print "Unable to create Tag: ", post
                        continue

                        
