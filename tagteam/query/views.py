from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from post.models import Post, Tag, PostTag
from django.shortcuts import get_object_or_404
from query.support_functions import strip_query, getposts, json_get
from query.support_cassandra import getposts_ca
from django.views.decorators.csrf import csrf_exempt
from query.configurations import POST_RETURN_LIMIT
import string
import urllib
import time

# Configurations for Query Processing
athena_url = 'http://athena.ndnxr.com/query/processquery/'
zeus_url = 'http://zeus.ndnxr.com/query/processquery/'

garfield_url = 'http://garfield.ndnxr.com/query/processquery/'

# Create your views here.

def index(request):
    if request.method == 'POST':
        p = Post.objects.get(id=1)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')

@csrf_exempt
def processquery(request):
    if request.method == 'POST' and request.POST.dict().has_key('query'):
        query = request.POST.get('query', '')

        # Controller::Application query logic here
        if not query.strip():
            return HttpResponse('Query is blank.')
       
        # Strip query to ensure that it is valid and get sets
        addset, removeset, valid_query = strip_query(query)

        if not valid_query:
            return HttpResponse('Invalid query.')

        # Get top POST_RETURN_LIMIT most recent post within addset-removeset
        start = time.time()
        post_results, err_msg = getposts(addset, removeset, POST_RETURN_LIMIT)
        end   = time.time()

        time_diff = end - start

        # Insert err_msg followed by time
        post_results.insert(0, Post(text=err_msg)) 
        post_results.insert(0, Post(text=time_diff)) 

        # Return JSON response of query logic
        data = serializers.serialize("json", post_results)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')


@csrf_exempt
def processqueryca(request):
    if request.method == 'POST' and request.POST.dict().has_key('query'):
        query = request.POST.get('query', '')

        # Controller::Application query logic here
        if not query.strip():
            return HttpResponse('Query is blank.')
       
        # Strip query to ensure that it is valid and get sets
        addset, removeset, valid_query = strip_query(query)

        if not valid_query:
            return HttpResponse('Invalid query.')

        # Get top POST_RETURN_LIMIT most recent post within addset-removeset
        #start = time.time()
        post_results, err_msg, time_diff = getposts_ca(addset, removeset, POST_RETURN_LIMIT)
        #end   = time.time()

        #time_diff = end - start

        # Insert err_msg followed by time
        post_results.insert(0, Post(text=err_msg)) 
        post_results.insert(0, Post(text=time_diff)) 

        # Return JSON response of query logic
        data = serializers.serialize("json", post_results)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('Invalid request.')




def getpost(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    data = serializers.serialize("json", [p])
    return HttpResponse(data, content_type="application/json")

def getzeuspost(request, post_id):
    f = urllib.urlopen(zeus_getpost_url + post_id)
    reply = '';

    for line in f:
        reply += line

    f.close()

    return HttpResponse(reply, content_type="application/json")

def getmoreobjects(request):
    p = Posts.objects.filter(text__contains='ivan')[:3]
    return HttpResponse("getmoreobjects() not implemente.")

# Proecess query request
# Athena MySQL 
@csrf_exempt
def apq(request):
    return json_get(request, athena_url)

# Zeus MySQL
@csrf_exempt
def zpq(request):
    return json_get(request, zeus_url)

# Garfield and Odie Cassandra
@csrf_exempt
def gopq(request):
    return json_get(request, garfield_url)

# Distributed MySQL (Athena & Zeus)
@csrf_exempt
def processquerydist(request):
    # FIXME: Parallelize these queries
    
    # Get Athena post objects
    ajson = apq(request).content

    aposts = []
    for p in serializers.deserialize("json", ajson):
        aposts.append(p.object)

    # Get Zeus post objects
    zjson = zpq(request).content

    zposts = []
    for p in serializers.deserialize("json", zjson):
        zposts.append(p.object)

    # Get time and err_msg if any
    a_post_time = aposts.pop(0).text
    z_post_time = zposts.pop(0).text

    # Error message NOT used here. Taken care of with Minerva's monolithic 
    # MySQL server. But we return them nonetheless for debugging purposes.
    a_err_msg = aposts.pop(0).text
    z_err_msg = zposts.pop(0).text

    # Build error message and get execution time: max of both exec time
    err_msg = ", ".join([a_err_msg, z_err_msg])
    time_diff = max(float(a_post_time), float(z_post_time))

    # Append to form all posts
    posts = []
    posts.extend(aposts)
    posts.extend(zposts)

    # Order posts by id descendingly    
    posts = sorted(posts, key=lambda post: -post.id)

    # Get appropriate number of post results
    post_results = posts[:POST_RETURN_LIMIT]

    # Insert err_msg followed by time
    post_results.insert(0, Post(text=err_msg)) 
    post_results.insert(0, Post(text=time_diff)) 

    # Return JSON response of query logic
    data = serializers.serialize("json", post_results)
    return HttpResponse(data, content_type="application/json")


