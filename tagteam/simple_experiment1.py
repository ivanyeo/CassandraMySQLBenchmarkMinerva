#!/usr/bin/python
import time
from post.models import Post, Tag, PostTag
import re

# Query: #ivan - #school
addset = ['ivan']
#removeset = ['it','general','other', 'popov','son','says']
removeset = []

def getposts(addset,removeset, topcnt):

    cnt = 0
    clean_posts = []  
    
    #Remove posts with tag from removeset
    emptyrm =  not removeset
    if not emptyrm:
        remove_str = "|".join(removeset)
        pattern = re.compile('#({0})'.format(remove_str))

    while len(clean_posts) < topcnt:
        
        pids = set()

        #Retrieve top cnt to cnt+10 from each addtag
        for addtag in addset:
            pts = Tag.objects.get(value=addtag).posttag_set.all().order_by('-pid')[cnt:cnt+topcnt]
            pids = pids.union({ps.pid_id for ps in pts})

        post_results = Post.objects.filter(id__in=pids) 
        post_results = sorted(post_results, key=lambda post: -post.id)
        post_texts = [p.text for p in post_results]
        
        #Remove post if removeset is not empty
        if not emptyrm:
            for post in post_texts:
                if not pattern.findall(post):
                    clean_posts.append(post)
        else:
            clean_posts = post_texts

        #Add cnt for next round of data retrieval
        cnt = cnt+ topcnt
    return clean_posts

clean_posts = getposts(addset,removeset,10)
count=1
for po in clean_posts:
    print count,po    
    count+=1
