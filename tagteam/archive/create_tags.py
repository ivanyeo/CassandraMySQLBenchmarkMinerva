#!/usr/bin/python
"""
File that creates the Tag in the mysql Djano model
as well as links the post to the tag in the PostTag
mysql relation of the Django model.

This file is run with pexpect to initialize the
Django environment.
"""
from os import listdir
from os.path import isfile, join, getsize
from post.models import Post, Tag, PostTag
import sys
import re

# Configuration
posts_per_query = 10

start_idx = 0
end_idx = start_idx + posts_per_query

# RegEx for hash tags: #tag #another-tag
p = re.compile(r'#[\w|-]+')

# Get initial 10 posts
posts = Post.objects.all()[start_idx:end_idx]

while posts:
    # Go through each post and create the relevant Tag
    for post in posts:
        # Get all tags
        tags = p.findall(post.text)

        for tag in tags:
            try:
                t, created = Tag.objects.get_or_create(value=tag[1:])

                try:
                    PostTag.objects.create(pid=post, tid=t)
                except Exception:
                    print "Error in creating PostTag: ", post, tag
            except Exception:
                print "Error in creating Tag: ", tag

        #print post.id, ": ", post
        #print "\t-> ", tags

        #print "Added tags: ", tags

    #raw_input()

    # Get next set of posts to process
    start_idx = end_idx
    end_idx += posts_per_query
    posts = Post.objects.all()[start_idx:end_idx]

