#!/usr/bin/python
import time
from post.models import Post, Tag, PostTag
import re

# Query: #ivan - #school

# Experiment: Take 10 post items and get all tags
start = time.time()

post_tags = Tag.objects.get(value='ivan').posttag_set.all()[:10]
post_texts = [ pt.pid.text for pt in post_tags if 'school' in pt.pid.text ] 

'''
p = re.compile(r'[+|-]?\s*?#[\w|-]+')

rs = set()
for line in post_texts:
    rs = rs.union(set(p.findall(line)))
'''

end = time.time()
print (end - start)
print "Answers: ", post_texts
#print "Your set: "
#print rs

# Experiment: Take 10 post items and from each side
start = time.time()

# Get post tags
pt_1 = Tag.objects.get(value='ivan').posttag_set.all()[:10]
pt_2 = Tag.objects.get(value='school').posttag_set.all()[:10]

pt_1_pids = set([ item.pid_id for item in pt_1 ])
pt_2_pids = set([ item.pid_id for item in pt_2 ])

rs = pt_1_pids - pt_2_pids

results = []
for item in rs:
    results.append(Post.objects.get(id=item))

results = [ p.text for p in results ]

end = time.time()
print (end - start)
print results


